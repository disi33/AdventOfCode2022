import re

class InputToken:
  def __init__(self, type, content):
    self.type = type
    self.content = content

  def copy(self):
    return InputToken(self.type, self.content)

class TokenDefinition:
  def __init__(self, definition):
    self.definition = definition

  def match(self, input):
    match = re.match(f"^{self.definition}$", input)
    if match:
      return True
    return False

class Lexer:
  def __init__(self, tokenDefinitions, debug = False):
    self.debug = debug
    self.tokenDefinitions = tokenDefinitions
    self.tokenStream = []

  def consumeLine(self, line):
    chunks = line.strip().split(" ")
    foundMatch = False
    for chunk in chunks:
      if chunk.strip() == "":
        continue
      for tokenDefinition in self.tokenDefinitions.keys():
        tDef = self.tokenDefinitions[tokenDefinition]
        if tDef.match(chunk):
          self.tokenStream.append(InputToken(tokenDefinition, chunk))
          foundMatch = True
          if self.debug:
            print(f"[Lexer] found match for input '{chunk}' in '{tokenDefinition}'")
          break
      if not foundMatch:
        raise RuntimeError(f"Did not find token match for input '{chunk}'")

class ParseHelper:
  def findOuterMostBrackets(inputString):
    bracketPairs = []
    index = 0
    currentLevel = 0
    nextStart = -1
    while index < len(inputString):
      if inputString[index] == "(":
        currentLevel += 1
        if currentLevel == 1:
          nextStart = index
      if inputString[index] == ")":
        currentLevel -= 1
        if currentLevel == 0:
          bracketPairs.insert(0, (nextStart, index))
          nextStart = -1
      index += 1
    return bracketPairs

internalCounters = {}

class NamingHelper:
  def getUniqueInternalName(chunk = "rule"):
    if not chunk in internalCounters.keys():
      internalCounters[chunk] = 1
    else:
      internalCounters[chunk] += 1
    return f"_{chunk}_{internalCounters[chunk]}"

class ParseContext:
  def __init__(self, tokenDefinitions, grammar, actions, tokenStream, lookahead = 1, debug = False):
    self.tokenDefinitions = tokenDefinitions
    self.grammar = grammar
    self.actions = actions
    self.tempGrammar = {}
    self.tokenStream = tokenStream
    self.requiredLookahead = lookahead
    self.debug = debug

  def addGrammarRule(self, name, rule):
    self.tempGrammar[name] = rule

  def getLookaheadTokenStream(self):
    laStream = []
    i = 0
    while i < self.requiredLookahead and i < len(self.tokenStream):
      laStream.append(self.tokenStream[i])
      i += 1
    return laStream

  def findRuleByName(self, name): 
    if name in self.grammar.keys():
      return self.grammar[name]
    elif name in self.tempGrammar.keys():
      return self.tempGrammar[name]
    raise NotImplementedError(f"Unable to resolve rule by name '{name}'")

  def findTokenDefinitionByName(self, name):
    if name in self.tokenDefinitions.keys():
      return self.tokenDefinitions[name]
    raise NotImplementedError()

  def copy(self):
    newCopy =  ParseContext(self.tokenDefinitions, self.grammar.copy(), self.tokenStream.copy(), self.actions, self.requiredLookahead, self.debug)
    for tempGrammarRule in self.tempGrammar.keys():
      newCopy.addGrammarRule(tempGrammarRule, self.tempGrammar[tempGrammarRule])
    return newCopy

class ParseState:
  def __init__(self):
    self.state = {}

  def add(self, name, value):
    self.state[name] = value

  def consume(self, otherContext, overwriteExisting = False):
    if otherContext is None:
      return
    for k,v in otherContext.state.items():
      if not overwriteExisting and k in self.state.keys():
        continue
      self.add(k, v)

class GrammarParser:
  def lookahead(self, tokens, parseContext):
    raise NotImplementedError()
  
  def match(self, parseContext, parentState):
    raise NotImplementedError()

class AtomicTokenParser(GrammarParser):
  def __init__(self, definition):
    self.definition = definition

  def lookahead(self, tokens, parseContext):
    if type(tokens) == list and len(tokens) == 0:
      return True, tokens
    tokenToCheck = tokens
    if type(tokenToCheck) == list:
      tokenToCheck = tokenToCheck[0]
    if parseContext.debug:
      print(f"[Parser] Attempt to match token '{tokenToCheck.type}' against definition '{self.definition}'")
    if tokenToCheck.type == self.definition:
      newTokens = tokens.copy() if type(tokens) == list else None
      if type(tokens) == list:
        del newTokens[0]
      return True, newTokens
    return False, tokens
  
  def match(self, parseContext, parentState):
    if not self.lookahead(parseContext.tokenStream[0], parseContext):
      raise RuntimeError()
    tokenToConsume = parseContext.tokenStream[0].copy()
    if parseContext.debug:
      print(f"[Parser] matched token '{tokenToConsume.type}' with value '{tokenToConsume.content}'")
    del parseContext.tokenStream[0]
    return tokenToConsume.content, None

class CommandParser(GrammarParser):
  def __init__(self, definition):
    self.definition = definition

  def lookahead(self, tokens, parseContext):
    # ignore lookahead for command instructions
    return True, tokens
  
  def match(self, parseContext, parentState):
    parseContext.actions[self.definition](parentState.state)
    return "", None

class RuleReferenceParser(GrammarParser):
  def __init__(self, definition):
    self.definition = definition

  def lookahead(self, tokens, parseContext):
    return parseContext.findRuleByName(self.definition).lookahead(tokens, parseContext)
  
  def match(self, parseContext, parentState):
    return parseContext.findRuleByName(self.definition).match(parseContext, parentState)

class TerminalTokenParser(GrammarParser):
  def __init__(self, definition):
    self.definition = definition
    self.variableName = ""
    if "=" in self.definition:
      splitDefinition = self.definition.split("=")
      self.variableName = splitDefinition[0]
      self.definition = splitDefinition[1]

    if "t:" in self.definition:
      parserDefinition = self.definition.replace("t:", "")
      self.parser = AtomicTokenParser(parserDefinition)
    elif self.definition.startswith("<") and self.definition.endswith(">"):
      commandDefinition = self.definition.replace("<", "").replace(">", "")
      self.parser = CommandParser(commandDefinition)
    else:
      self.parser = RuleReferenceParser(self.definition)

  def lookahead(self, tokens, parseContext):
    return self.parser.lookahead(tokens, parseContext)
  
  def match(self, parseContext, parentState):
    newState = ParseState()
    textOutput, state = self.parser.match(parseContext, parentState)
    newState.consume(state)
    if self.variableName != "":
      if parseContext.debug:
        print(f"[Parser][Context] Adding variable {self.variableName} with content: '{textOutput}'")
      newState.add(self.variableName, textOutput)
    return textOutput, newState

class RepetitionParser(GrammarParser):
  def __init__(self, definition):
    self.definition = definition
    self.parser = TerminalTokenParser(definition)

  def lookahead(self, tokens, parseContext):
    remainingTokens = tokens
    while len(remainingTokens) > 0:
      success, remainingTokens = self.parser.lookahead(remainingTokens, parseContext.copy())
      if not success:
        return success, remainingTokens
    return True, remainingTokens
  
  def match(self, parseContext, parentState):
    state = ParseState()
    state.consume(parentState)
    success, remainingTokens = self.lookahead(parseContext.getLookaheadTokenStream(), parseContext)
    if not success:
      raise RuntimeError()
    output, childState = self.parser.match(parseContext, state)
    state.consume(childState)
    success, remainingTokens = self.lookahead(parseContext.getLookaheadTokenStream(), parseContext)
    while success and len(parseContext.tokenStream) > 0:
      subSequentOutput, subSequentChildState = self.parser.match(parseContext, state)
      state.consume(subSequentChildState, True)
      output += " " + subSequentOutput
      success, remainingTokens = self.lookahead(parseContext.getLookaheadTokenStream(), parseContext)
    return output, state

class SequenceParser(GrammarParser):
  def __init__(self, definition):
    self.definition = definition
    self.sequenceDefinitions = definition.split(" ")
    self.sequence = []
    for definition in self.sequenceDefinitions:
      if definition.strip() == "":
        continue
      if definition.endswith("+"):
        self.sequence.append(RepetitionParser(definition.replace("+", "")))
      else:
        self.sequence.append(TerminalTokenParser(definition))

  def lookahead(self, tokens, parseContext):
    remainingTokens = tokens
    for sequenceItem in self.sequence:
      success, remainingTokens = sequenceItem.lookahead(remainingTokens, parseContext.copy())
      if not success:
        return success, remainingTokens
      if len(remainingTokens) == 0:
        break
    return True, remainingTokens
  
  def match(self, parseContext, parentState):
    if not self.lookahead(parseContext.getLookaheadTokenStream(), parseContext):
      raise RuntimeError()
    output = ""
    state = ParseState()
    state.consume(parentState)
    for sequenceItem in self.sequence:
      sequenceOutput, sequenceState = sequenceItem.match(parseContext, state)
      output += sequenceOutput + " "
      state.consume(sequenceState, True)
    return output.strip(), state

class OptionParser(GrammarParser):
  def __init__(self, definition):
    self.optionDefinitions = definition.split("|")
    self.options = []
    for definition in self.optionDefinitions:
      self.options.append(SequenceParser(definition.strip()))

  def lookahead(self, tokens, parseContext):
    if parseContext.debug and len(self.options) > 1:
      print(f"[Parser][Options] Checking '{len(self.options)}' options")
    for option in self.options:
      success, remainingTokens = option.lookahead(tokens, parseContext.copy())
      if parseContext.debug:
        print(f"[Parser][Options] Lookahead for option '{option.definition}' was successful? {success}")
        # print(f"[Parser][Options] Next token is '{parseContext.tokenStream[0].content}'")
      if success:
        return success, remainingTokens
    return False, tokens
  
  def match(self, parseContext, parseState):
    for option in self.options:
      success, remainingTokens = option.lookahead(parseContext.getLookaheadTokenStream(), parseContext)
      if success:
        return option.match(parseContext, parseState)
    raise RuntimeError("No option matched")

class GrammarRuleDefinition:
  def __init__(self, name, definition, isInternal = False):
    self.name = name
    self.definition = definition
    # we handle groupings with parentheses by making them internal sub grammar rules
    # those need to be saved and considered when matching these rules
    self.internalRuleDefinitions = {}
    self.isInternal = isInternal

    # first find all groupings and turn them into subrules
    brackets = ParseHelper.findOuterMostBrackets(definition)
    for bracketPairIndices in brackets:
      startIndex, endIndex = bracketPairIndices
      startString = self.definition[:startIndex]
      subRuleString = self.definition[startIndex+1:endIndex]
      endString = self.definition[endIndex+1:]
      subruleName = NamingHelper.getUniqueInternalName()
      subRule = GrammarRuleDefinition(subruleName, subRuleString)
      self.internalRuleDefinitions[subruleName] = subRule 
      self.definition = startString + subruleName + endString

    self.parser = OptionParser(self.definition)

  def lookahead(self, tokens, parseContext):
    for customRule in self.internalRuleDefinitions:
      parseContext.addGrammarRule(customRule, self.internalRuleDefinitions[customRule])
    return self.parser.lookahead(tokens, parseContext)
  
  def match(self, parseContext, parentState):
    # if this is an internal helper we need to make the parent state available, otherwise create new state
    state = parentState if self.isInternal else ParseState()

    if parseContext.debug:
      print(f"[Parser] Matching rule '{self.name}'")
    success, remainingTokens = self.lookahead(parseContext.getLookaheadTokenStream(), parseContext)
    if success:
      if parseContext.debug:
        print(f"[Parser] Finished parsing rule '{self.name}'")
      return self.parser.match(parseContext, state)
    else:
      raise RuntimeError(f"Required lookahead failed, next token is: {remainingTokens[0].type}")

class Parser:
  def __init__(self, tokenDefinitions, ruleDefinitions, actions, entryPoint, inputLines, requiredLookahead = 1, debug = False):
    self.tokenDefinitions = {}
    for token in tokenDefinitions.keys():
      self.tokenDefinitions[token] = TokenDefinition(tokenDefinitions[token])
    self.ruleDefinitions = {}
    for rule in ruleDefinitions.keys():
      self.ruleDefinitions[rule] = GrammarRuleDefinition(rule, ruleDefinitions[rule])
    self.actions = actions
    self.entryPoint = entryPoint
    self.lexer = Lexer(self.tokenDefinitions, debug)
    self.debug = debug
    self.requiredLookahead = requiredLookahead
    for line in inputLines:
      self.lexer.consumeLine(line)

  def parse(self):
    parseContext = ParseContext(self.tokenDefinitions, self.ruleDefinitions, self.actions, self.lexer.tokenStream.copy(), self.requiredLookahead, self.debug)
    entryPoint = self.ruleDefinitions[self.entryPoint]
    entryPoint.match(parseContext, ParseState())
    if parseContext.debug:
      print("Finished parsing!")
      if len(parseContext.tokenStream) > 0:
        print(f"!!! Did not parse entire input, remaining tokens: {len(parseContext.tokenStream)}")