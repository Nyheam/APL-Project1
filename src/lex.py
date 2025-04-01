import ply.lex as lex 
from output import output_handler

tokens = (
    'RESERVE',
    'CONFIRM',
    'PAY',
    'CANCEL',
    'SHOW',
    'AVAILABLE',
    'BOOKINGS',
    'FOR',
    'ON',
    'QUANTITY',
    'USING',
    'BOOKING',
    'TICKET_TYPE', # e.g., concert, train ticket
    'EVENT_NAME',
    'DATE',
    'INTEGER',
    'BOOKING_REFERENCE',
    'PAYMENT_METHOD',
    'STRING',
    'ID'
)

# Literals (not strictly needed for this grammar, but good practice for extendability)
literals = []

# Reserved words - Keywords
reserved_words = {
    'reserve': 'RESERVE',
    'confirm': 'CONFIRM',
    'pay': 'PAY',
    'cancel': 'CANCEL',
    'show': 'SHOW',
    'available': 'AVAILABLE',
    'bookings': 'BOOKINGS',
    'for': 'FOR',
    'on': 'ON',
    'quantity': 'QUANTITY',
    'using': 'USING',
    'booking': 'BOOKING'
}

# Define t_TICKET_TYPE *BEFORE* t_ID (Rule Ordering - Key Fix)
def t_TICKET_TYPE(t):
    r'(concert|train\sticket|bus\sticket|airline\sticket|football\smatch)' # Regex is fine, rule order is key
    return t

def t_PAYMENT_METHOD(t):
    r'(credit\scard|debit\scard|paypal)'
    return t

def t_BOOKING_REFERENCE(t):
    r'"[A-Z0-9]+"' # Example Booking Ref format, adjust as needed
    t.value = t.value[1:-1] # Remove quotes
    return t

def t_EVENT_NAME(t):
    r'"[^"]+"'
    t.value = t.value[1:-1]
    return t

def t_DATE(t):
    r'\(\d{4}-\d{2}-\d{2}\)' # Example date format YYYY-MM-DD, can be more flexible
    t.value = t.value[1:-1]
    return t

def t_STRING(t):
    r'"[^"]+"' # General string, for extendability and potential errors
    t.value = t.value[1:-1]
    return t


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define t_ID *AFTER* t_TICKET_TYPE
def t_ID(t): # For keywords and future variables (if needed)
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    keyword_type = reserved_words.get(t.value) # Get token type if it's a keyword, else None
    if keyword_type:
        t.type = keyword_type # Use keyword token type
    else:
        t.type = 'ID' # Otherwise, it's a generic ID token
    return t


t_ignore = ' \t\n' # Ignore spaces, tabs, and newlines

def t_error(t):
    #print(f"Lexical error: Illegal character '{t.value[0]}'")
    output_handler(f"Lexical error: Illegal character '{t.value[0]}' at position {t.lexpos}") # Use output_handler
    t.lexer.skip(1)

lexer = lex.lex()
