
from yacc import *
import mysql.connector
from db_con import connect_to_db, close_db_connection # Import from database_utils
from output import output_handler

class SemanticAnalyzer:
    def __init__(self): # Removed db_connection argument from __init__
        self.valid_ticket_types = ["concert", "train ticket", "bus ticket", "airline ticket", "football match"]
        # self.bookings = {} # Removed: No longer using in-memory bookings for semantic checks
        self.db_connection = connect_to_db() # Establish connection in SemanticAnalyzer's init

        if not self.db_connection: # Check if database connection was successful
            print("Warning: Database connection failed in SemanticAnalyzer. Semantic checks involving database will not function.")
            output_handler("Warning: Database connection failed in SemanticAnalyzer. Semantic checks involving database will not function.")

    def __del__(self): # Add destructor to ensure connection is closed when SemanticAnalyzer is deleted
        close_db_connection(self.db_connection) # Close database connection when SemanticAnalyzer is destroyed


    def analyze(self, program):
        errors = []
        if not self.db_connection: # Check again at analysis time if DB connection is valid
            errors.append("Error: No database connection available for semantic analysis.")
            return errors # Stop analysis if no DB connection
        for statement in program.statements:
            if isinstance(statement, ReserveStatement):
                errors.extend(self._analyze_reserve(statement))
            elif isinstance(statement, ConfirmStatement):
                errors.extend(self._analyze_confirm(statement))
            elif isinstance(statement, PayStatement):
                errors.extend(self._analyze_pay(statement))
            elif isinstance(statement, CancelStatement):
                errors.extend(self._analyze_cancel(statement))
            elif isinstance(statement, ShowAvailableStatement):
                errors.extend(self._analyze_show_available(statement))
            elif isinstance(statement, ShowBookingsStatement):
                pass # No semantic checks needed for show bookings for now
            else:
                errors.append(f"Semantic Error: Unknown statement type: {statement}")
        return errors

    def _analyze_reserve(self, statement):
        errors = []
        if statement.ticket_type not in self.valid_ticket_types:
            errors.append(f"Semantic Error: Invalid ticket type '{statement.ticket_type}'. Valid types are: {', '.join(self.valid_ticket_types)}")
        try:
            quantity = int(statement.quantity)
            if quantity <= 0:
                errors.append(f"Semantic Error: Quantity must be a positive integer, but is '{statement.quantity}'")
        except ValueError:
            errors.append(f"Semantic Error: Quantity '{statement.quantity}' is not a valid integer.")
        return errors

    def _analyze_confirm(self, statement):
        errors = []
        booking_reference = statement.booking_reference

        # --- Semantic Check: Check if booking_reference exists in the database ---
        try:
            cursor = self.db_connection.cursor(dictionary=True) # Use self.db_connection
            sql = "SELECT BookingReference FROM Bookings WHERE BookingReference = %s"
            cursor.execute(sql, (booking_reference,))
            booking_record = cursor.fetchone()
            cursor.close()

            if not booking_record:
                errors.append(f"Booking reference '{booking_reference}' not found.")

        except mysql.connector.Error as db_err:
            errors.append(f"Database error during booking lookup: {db_err}")
        except Exception as e:
            errors.append(f"Error during booking reference check: {e}")
        # --- End Semantic Check ---

        return errors

    def _analyze_pay(self, statement):
        errors = []
        booking_reference = statement.booking_reference

        # --- Semantic Check: Check if booking_reference exists in the database ---
        try:
            cursor = self.db_connection.cursor(dictionary=True) # Use self.db_connection
            sql = "SELECT BookingReference FROM Bookings WHERE BookingReference = %s"
            cursor.execute(sql, (booking_reference,))
            booking_record = cursor.fetchone()
            cursor.close()

            if not booking_record:
                errors.append(f"Booking reference '{booking_reference}' not found.")
            if not statement.payment_method: # Basic check for payment method presence
                errors.append("Payment method is required for pay command.")

        except mysql.connector.Error as db_err:
            errors.append(f"Database error during booking lookup: {db_err}")
        except Exception as e:
            errors.append(f"Error during booking reference check: {e}")
        # --- End Semantic Check ---

        return errors

    def _analyze_cancel(self, statement):
        errors = []
        booking_reference = statement.booking_reference

        # --- Semantic Check: Check if booking_reference exists in the database ---
        try:
            cursor = self.db_connection.cursor(dictionary=True) # Use self.db_connection
            sql = "SELECT BookingReference FROM Bookings WHERE BookingReference = %s"
            cursor.execute(sql, (booking_reference,))
            booking_record = cursor.fetchone()
            cursor.close()

            if not booking_record:
                errors.append(f"Booking reference '{booking_reference}' not found.")

        except mysql.connector.Error as db_err:
            errors.append(f"Database error during booking lookup: {db_err}")
        except Exception as e:
            errors.append(f"Error during booking reference check: {e}")
        # --- End Semantic Check ---

        return errors

    def _analyze_show_available(self, statement):
        errors = []
        if statement.ticket_type not in self.valid_ticket_types:
            errors.append(f"Semantic Error: Invalid ticket type '{statement.ticket_type}'. Valid types are: {', '.join(self.valid_ticket_types)}")
        return errors
