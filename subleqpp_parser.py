 # Subleq++ Parser
 # Copyright (C) 2022 McChuck
 # original Copyright (C) 2013 Chris Lloyd
 # Released under GNU General Public License
 # See LICENSE for more details.
 # https://github.com/cjrl
 # lloyd.chris@verizon.net

 #  The first instruction be the start address of the code to execute.

 #  A B C    [B] -= [A], if [B]<=0 goto C
 #  A B      A B ?  (B -= A, goto next)
 #  A        A A ?  (A = 0, goto next)
 #  A !      print [A], goto next
 #  ! B      input [B], goto next
 #  A A !    halt
 #  A *B *C  [[B]] -= [A], if [[B]]<=0 goto [C]

 #  ?        next address
 #  @        this address
 #  label:   address label, cannot be the only thing on a line
 #  *label   pointer to address label, represented as a negative address
 #  !        0 used for input, output, and halting
 #  ;        end of instruction
 #  #        comment
 #  .        data indicator
 #  " or '   string delimeters, must be data


class Parser:

    tokens = []
    label_table = {}

    def parse(self, raw_string):
        raw_string = self.expand_literals(raw_string)
        raw_string = raw_string.replace('\n',';')
        raw_string = raw_string.replace('#',';#')
        raw_string = raw_string.replace(':',': ')
        raw_string = raw_string.replace('.','. ')
        raw_string = raw_string.replace('!', "0 ")
        self.tokens = [token.split() for token in raw_string.split(';') if not '#' in token and token.strip()]
        self.parse_labels()
        self.expand_instructions()
        self.update_labels()
        self.tokens = [token for token in sum(self.tokens,[]) if token != '.']
        self.resolve_labels()
        try:
            response = []
            for token in self.tokens:
                response.append(int(token))
            return(response)
        except ValueError:
            print("Unmatched label:", token, flush=True)
            raise

    def resolve_labels(self):
        try:
            for i, token in enumerate(self.tokens):
                modifier = 0
                plus = token.find('+')
                minus = token.find('-')
                if plus > 0:
                    modifier = int(token[plus:])
                    token = token[:plus]
                elif minus > 0:
                    modifier = int(token[minus:])
                    token = token[:minus]
                if token == '?':     # next IP
                        self.tokens[i] = i+1+modifier
                elif token == '@':   # this IP
                        self.tokens[i] = i+modifier
                elif token[0] == "*":     # pointer
                    token = token[1:]
                    if token in self.label_table:
                        self.tokens[i] = -(self.label_table[token]+modifier)
                else:
                    if token in self.label_table:
                        self.tokens[i] = self.label_table[token]+modifier
        except:
            print("\nError resolving label: ", token, " @ ", i, flush=True)
            raise


    def update_labels(self):
        for i, label in enumerate(self.label_table):
            self.label_table[label] = self.get_label_index(label)

    def get_label_index(self,label):
        index = 0
        address, x = self.label_table[label]
        for i in range(address):
            index += len(self.tokens[i])
            if '.' in self.tokens[i][0]:
                index -= 1 
        if '.' in self.tokens[address][0]:
            return index + x - 1
        return index

    def expand_instructions(self):
        self.tokens[0].insert(0, '.')
        for token_index, token in enumerate(self.tokens):
            if not token[0] == '.':
                operands = [token[0],token[0],'?']
                for i, operand in enumerate(token):
                    operands[i] = operand
                self.tokens[token_index] = operands

    def parse_labels(self):
        for token_index, token in enumerate(self.tokens):
            if len(token) == 1 and token[0][-1] == ':':                         # correcting for lone label
                token.extend(self.tokens[token_index+1])
                self.tokens.pop(token_index+1)
            for operand_index, operand in enumerate(token):
                if operand[-1] == ':':
                    token.remove(operand)
                    operand = operand[:-1]
                    self.label_table[operand] = (token_index, operand_index)


    def expand_literals(self,raw_string):
        in_dq_literal = False       # "
        in_sq_literal = False       # '
        in_comment  = False
        expanded_raw_string = ""
        for char in raw_string:
            if char == "#" and not in_sq_literal and not in_dq_literal:
                in_comment = True
            if in_comment:
                if ord(char) == 10 or ord(char) == 13:
                    in_comment = False
                else:
                    char = ""
            if char == '"' and not in_sq_literal:
                in_dq_literal ^= True
            elif char == "'" and not in_dq_literal:
                in_sq_literal ^= True
            elif in_dq_literal or in_sq_literal:
                expanded_raw_string += str(ord(char)) + ' '
            else:
                expanded_raw_string += char
        return expanded_raw_string
