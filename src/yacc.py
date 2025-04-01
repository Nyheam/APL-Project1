import ply.yacc as yacc
from lex import tokens, lexer # Import tokens from lex.py
from output import output_handler
# ast.py (Abstract Syntax Tree Definitions)



class Program(object):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements})"

class ReserveStatement(object):
    def __init__(self, ticket_type, event_name, date, quantity):
        self.ticket_type = ticket_type
        self.event_name = event_name
        self.date = date
        self.quantity = quantity

    def __repr__(self):
        return f"ReserveStatement(ticket_type='{self.ticket_type}', event_name='{self.event_name}', date='{self.date}', quantity={self.quantity})"


class ConfirmStatement(object):
    def __init__(self, booking_reference):
        self.booking_reference = booking_reference

    def __repr__(self):
        return f"ConfirmStatement(booking_reference='{self.booking_reference}')"

class PayStatement(object):
    def __init__(self, booking_reference, payment_method):
        self.booking_reference = booking_reference
        self.payment_method = payment_method

    def __repr__(self):
        return f"PayStatement(booking_reference='{self.booking_reference}', payment_method='{self.payment_method}')"

class CancelStatement(object):
    def __init__(self, booking_reference):
        self.booking_reference = booking_reference

    def __repr__(self):
        return f"CancelStatement(booking_reference='{self.booking_reference}')"

class ShowAvailableStatement(object):
    def __init__(self, ticket_type):
        self.ticket_type = ticket_type

    def __repr__(self):
        return f"ShowAvailableStatement(ticket_type='{self.ticket_type}')"

class ShowBookingsStatement(object):
    def __init__(self):
        pass # No arguments for now

    def __repr__(self):
        return "ShowBookingsStatement()"

def p_program(p):
    '''program : statement_list'''
    p[0] = Program(p[1])

def p_statement_list(p):
    '''statement_list : statement statement_list
                      | statement'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : reserve_statement
                 | confirm_statement
                 | pay_statement
                 | cancel_statement
                 | show_available_statement
                 | show_bookings_statement'''
    p[0] = p[1]

def p_reserve_statement(p):
    '''reserve_statement : RESERVE TICKET_TYPE FOR EVENT_NAME ON DATE QUANTITY INTEGER'''
    p[0] = ReserveStatement(p[2], p[4], p[6], p[8])

def p_confirm_statement(p):
    '''confirm_statement : CONFIRM BOOKING BOOKING_REFERENCE'''
    p[0] = ConfirmStatement(p[3])

def p_pay_statement(p):
    '''pay_statement : PAY FOR BOOKING BOOKING_REFERENCE USING PAYMENT_METHOD'''
    p[0] = PayStatement(p[4], p[6])

def p_cancel_statement(p):
    '''cancel_statement : CANCEL BOOKING BOOKING_REFERENCE'''
    p[0] = CancelStatement(p[3])

def p_show_available_statement(p):
    '''show_available_statement : SHOW AVAILABLE TICKET_TYPE'''
    p[0] = ShowAvailableStatement(p[3])

def p_show_bookings_statement(p):
    '''show_bookings_statement : SHOW BOOKINGS'''
    p[0] = ShowBookingsStatement()

def p_error(p):
    if p:
        output_handler(f"Syntax error at token '{p.type}' (value '{p.value}') on line {p.lineno}")
        print(f"Syntax error at token '{p.type}' (value '{p.value}') on line {p.lineno}")
    else:
        output_handler("Syntax error at EOF")
        print("Syntax error at EOF")
    


parser = yacc.yacc()
