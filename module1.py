import ply.lex as lex #Импортирование библиотеки PLY

#Выражение оператора CREATE POLICY
#CREATE POLICY name ON table_name
#    [ FOR { ALL | SELECT | INSERT | UPDATE | DELETE } ]
#    [ TO { role_name | PUBLIC | CURRENT_USER | SESSION_USER } [, ...] ]
#    [ USING ( using_expression ) ]
#    [ WITH CHECK ( check_expression ) ]

#Создание массива токенов
tokens = ("CREATE_P", "ON", "FOR", "ALL", "SELECT", "INSERT", "UPDATE",
	"DELETE", "TO", "PUBLIC", "CURRENT_USER", "SESSION_USER", "USING", "WITH_C",
	"NAME", "EQUAL", "BRK_OPEN", "BRK_CLOSE", "EXP_END", "COMMA")

#Описание каждого члена массива токенов при помощи регулярных выражений
ident = r"[a-z]\w*\s*\=*\s*[a-z]\w*"
t_EQUAL = "\="
t_ignore = " \t"
t_CREATE_P = r"\CREATE[ ]+POLICY"
t_ON = r"ON"
t_FOR = r"FOR"
t_ALL = r"ALL"
t_SELECT = r"SELECT"
t_INSERT = r"INSERT"
t_UPDATE = r"UPDATE"
t_DELETE = r"DELETE"
t_TO = r"TO"
t_PUBLIC = r"PUBLIC"
t_CURRENT_USER = r"\CURRENT_USER"
t_SESSION_USER = r"\SESSION_USER"
t_USING = r"USING"
t_WITH_C = r"WITH[ ]+CHECK"
t_NAME = ident
t_BRK_OPEN = r"\("
t_BRK_CLOSE = r"\)"
t_EXP_END = r"\;"
t_COMMA = r"\,"
#Метод для обработки цифр
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t
#Метод для обработки новой линии
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
#Метод обработки ошибки
def t_error(t):
    print('Illegal character {0}'.format(t.value[0]))
    t.lexe.skip(1)

lexer = lex.lex()

import ply.yacc as yacc
#Создание класса для Node
class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            st.append( str( part ) )
        return "\n".join(st)

    def __repr__(self):
        return self.type + "|" + self.parts_str().replace("\n", "\n|")

    def __init__(self, type, parts):
        self.type = type
        self.parts = parts
# Создание основного метода для CREATE POLICY
def p_create(p):
	'''create : CREATE_P name ON table_name for to using with_c EXP_END'''
	p[0] = Node('',[p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9]])
# Метод для обработки имени политики
def p_name(p):
	'''name : NAME'''
	p[0] = Node('', [p[1]])
# Метод для обработки имени таблицы к которой применяется политика
def p_table_name(p):
	'''table_name : NAME'''
	p[0] = Node('', [p[1]])
# Метод для обработки FOR
def p_for(p):
    '''for :
			| FOR a_s_i_u_d'''
    if len(p) == 1:
         p[0] = Node('', ["None FOR"])
    else:
        p[0] = Node('', [p[1], p[2]])
# Метод, который выбирает одну из команд
def p_a_s_i_u_d(p):
	'''a_s_i_u_d : ALL
			| SELECT
			| INSERT
			| UPDATE
			| DELETE'''
	p[0] = Node('', [p[1]])
# Метод для обработки TO
def p_to(p):
    '''to :
			| TO param_comma'''
    if len(p) == 1:
        p[0] = Node('', ["None TO"])
    else:
        p[0] = Node('', [p[1], p[2]])
# Метод, который позволяет указывать несколько команд в TO через запятую
def p_param_comma(p):
	'''param_comma : NAME comma
				| PUBLIC comma
				| CURRENT_USER comma
				| SESSION_USER comma'''
	p[0] = Node('', [p[1], p[2]])
# Метод для обработки запятой
def p_comma(p):
    '''comma :
				| param_comma'''
    if len(p) == 1:
        p[0] = Node('', ["None COMMA"])
    else:
        p[0] = Node('', [p[1]])
# Метод для обработки USING
def p_using(p):
    '''using :
			| USING BRK_OPEN NAME BRK_CLOSE'''
    if len(p) == 1:
        p[0] = Node('', ["None USING"])
    else:
        p[0] = Node('', [p[1], p[2], p[3], p[4]])
# Метод для обработки WITH CHECK
def p_with_c(p):
    '''with_c :
            | WITH_C BRK_OPEN NAME BRK_CLOSE'''
    if len(p) == 1:
        p[0] = Node('', ["None WITH_CHECK"])
    else:
        p[0] = Node('', [p[1], p[2], p[3], p[4]])
# Метод для обработки ошибки
def p_error(p):
    print('syntax error in line {0}'.format(p.lineno))
    yacc.errok()

yacc.yacc()
# Входные данные для программы
data = ''' CREATE POLICY user_mod ON passwd FOR UPDATE TO PUBLIC
  USING (current_user = user_name)
  WITH CHECK (current_user = user_name); '''

if __name__ == '__main__':
    print("Data:\n", data, "\n\nLex analize:")
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
    print("\nYacc analize:")
    result = yacc.parse(data)
    print(result)
    print("No errors in lex and yacc.")


