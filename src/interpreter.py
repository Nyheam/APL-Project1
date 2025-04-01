# interpreter.py
import uuid
import mysql.connector  # Changed import
from yacc import *
import google.generativeai as genai # Import the Gemini API library
import os
from dotenv import load_dotenv  # Import load_dotenv


load_dotenv()  # Load environment variables from .env file

class Interpreter:
    def __init__(self, semantic_analyzer):
        self.semantic_analyzer = semantic_analyzer
        self.conn = None
        self.cursor = None
        self._connect_to_db()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY") # Use a different environment variable name
        if not self.gemini_api_key:
            print("Error: GEMINI_API_KEY environment variable not set. LLM features will be limited.")
            output_handler("Error: GEMINI_API_KEY environment variable not set. LLM features will be limited.")
            self.gemini_api_key = None
    def _connect_to_db(self):
        try:
            # --- Replace with your MySQL connection details ---
            self.conn = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST"), # Get database details from environment variables
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=os.getenv("MYSQL_DATABASE")
                
            )
            self.cursor = self.conn.cursor(dictionary=True) # dictionary=True for fetching rows as dictionaries
            print("Connected to MySQL Database")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                output_handler("Something is wrong with your user name or password")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(f"Error connecting to database: {err}")
            self.conn = None


    def interpret(self, program):
        errors = self.semantic_analyzer.analyze(program)
        if errors:
            print("Semantic Analysis Errors:")
            output_handler("Semantic Analysis Errors:")
            for error in errors:
                print(f"  {error}")
            return

        if self.conn is None: # Check if database connection is established
            print("Error: No database connection. Cannot execute bookings.")
            output_handler("Error: No database connection. Cannot execute bookings.")
            return

        for statement in program.statements:
            if isinstance(statement, ReserveStatement):
                self._execute_reserve(statement)
            elif isinstance(statement, ConfirmStatement):
                self._execute_confirm(statement)
            elif isinstance(statement, PayStatement):
                self._execute_pay(statement)
            elif isinstance(statement, CancelStatement):
                self._execute_cancel(statement)
            elif isinstance(statement, ShowAvailableStatement):
                self._execute_show_available(statement)
            elif isinstance(statement, ShowBookingsStatement):
                self._execute_show_bookings(statement)

    def _execute_reserve(self, statement):
        booking_reference = f"BOOK{uuid.uuid4().hex[:8].upper()}" # Generate a unique booking ref
        try:
            sql = "INSERT INTO Bookings (BookingReference, TicketType, EventName, Date, Quantity, Status) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (booking_reference, statement.ticket_type, statement.event_name, statement.date, statement.quantity, "reserved")
            self.cursor.execute(sql, values)
            self.conn.commit() # Important to commit changes to the database
            print(f"Ticket reserved successfully. Booking Reference: '{booking_reference}'")
            output_handler(f"Ticket reserved successfully. Booking Reference: '{booking_reference}'")
        except mysql.connector.Error as ex:
            print(f"Database error during reservation: {ex}")
            output_handler(f"Database error during reservation: {ex}")
            self.conn.rollback() # Rollback on error to maintain data consistency


    def _execute_confirm(self, statement):
        booking_reference = statement.booking_reference
        try:
            sql = "UPDATE Bookings SET Status = %s WHERE BookingReference = %s"
            values = ("confirmed", booking_reference)
            self.cursor.execute(sql, values) # Execute the query
            row_count = self.cursor.rowcount  # Get rowcount AFTER execution
            if row_count > 0:
                self.conn.commit()
                print(f"Booking '{booking_reference}' confirmed.")
                output_handler(f"Booking '{booking_reference}' confirmed.")
            else:
                print(f"Error: Booking '{booking_reference}' not found in database.") # Database integrity check
                output_handler(f"Error: Booking '{booking_reference}' not found in database.")
            return row_count # Return row_count for potential future use or debugging
        except mysql.connector.Error as ex:
            print(f"Database error during confirmation: {ex}")
            output_handler(f"Database error during confirmation: {ex}")
            self.conn.rollback()
            return 0 # Return 0 to indicate failure


    def _execute_pay(self, statement):
        booking_reference = statement.booking_reference
        payment_method = statement.payment_method
        try:
            sql = "UPDATE Bookings SET Status = %s, PaymentMethod = %s WHERE BookingReference = %s"
            values = ("paid", payment_method, booking_reference)
            self.cursor.execute(sql, values) # Execute the query
            row_count = self.cursor.rowcount # Get rowcount AFTER execution
            if row_count > 0:
                self.conn.commit()
                print(f"Booking '{booking_reference}' paid using '{payment_method}'.")
                output_handler(f"Booking '{booking_reference}' paid using '{payment_method}'.")
            else:
                print(f"Error: Booking '{booking_reference}' not found in database for payment.")
                output_handler(f"Error: Booking '{booking_reference}' not found in database for payment.")
            return row_count # Return row_count
        except mysql.connector.Error as ex:
            print(f"Database error during payment: {ex}")
            output_handler(f"Database error during payment: {ex}")

            self.conn.rollback()
            return 0 # Return 0 for failure



    def _execute_cancel(self, statement):
        booking_reference = statement.booking_reference
        try:
            sql = "UPDATE Bookings SET Status = %s WHERE BookingReference = %s"
            values = ("cancelled", booking_reference)
            self.cursor.execute(sql, values) # Execute the query
            row_count = self.cursor.rowcount # Get rowcount AFTER execution
            if row_count > 0:
                self.conn.commit()
                print(f"Booking '{booking_reference}' cancelled.")
                output_handler(f"Booking '{booking_reference}' cancelled.")
            else:
                print(f"Error: Booking '{booking_reference}' not found in database for cancellation.")
                output_handler(f"Error: Booking '{booking_reference}' not found in database for cancellation.")
            return row_count # Return row_count
        except mysql.connector.Error as ex:
            print(f"Database error during cancellation: {ex}")
            output_handler(f"Database error during cancellation: {ex}")
            self.conn.rollback()
            return 0 # Return 0 for failure

    def _execute_show_available(self, statement):
        ticket_type = statement.ticket_type

        if not self.gemini_api_key: # Fallback if API key is not set
            print("Warning: Gemini API key not configured. Using simulated event data.")
            output_handler("Warning: Gemini API key not configured. Using simulated event data.")
            # ... (Simulated data fallback - if you still want it) ...
            print(f"No available events found for '{ticket_type}'.") # Basic fallback message for now
            output_handler(f"No available events found for '{ticket_type}'.")
            return

        genai.configure(api_key=self.gemini_api_key) # Configure Gemini API with your key
        model = genai.GenerativeModel('gemini-2.0-flash') # Choose the Gemini model

        try:
            prompt_gemini = f"List past {ticket_type} events or resources with dates, times, and A random number in Jamaica . Format the response as a clear, readable list. in the format Event name - the date in formant(YYY/MM/DD) - Random number " # Gemini prompt

            response = model.generate_content(prompt_gemini) # Generate content using Gemini

            llm_response_text = response.text # Get text response from Gemini

            print(f"Gemini LLM Response:\n{llm_response_text}\n--- End Gemini LLM Response ---") # Print raw Gemini response
            output_handler(f"Gemini LLM Response:\n{llm_response_text}\n--- End Gemini LLM Response ---")

            # --- Parse Gemini LLM Response (Adapt parsing for Gemini's output) ---
            events = self._parse_gemini_response(llm_response_text, ticket_type) # New parsing function for Gemini

            if events:
                print(f"Available {ticket_type}s:")
                for event in events:
                    print(f"- {event['name']} - {event['date']} - {event['availability']}") # Assuming parsed format
                    output_handler(f"- {event['name']} - {event['date']} - {event['availability']}")
            else:
                print(f"No available {ticket_type} events found based on Gemini response.")
                output_handler(f"No available {ticket_type} events found based on Gemini response.")


        except Exception as e: # Catching potential Gemini API errors and other issues
            print(f"Error communicating with Gemini API: {e}")
            output_handler(f"Error communicating with Gemini API: {e}")


    def _parse_gemini_response(self, llm_response_text, ticket_type): # Parsing function for Gemini output - Needs to be adapted
        """
        Parses the Gemini's text response to extract event details.
        This needs to be adapted based on Gemini's response format.
        This is still a basic example and needs improvement.
        """
        events = []
        lines = llm_response_text.strip().split('\n') # Split response into lines

        for line in lines:
            if line.strip(): # Ignore empty lines
                parts = line.split('-') # Simple split by '-' - may need to be adjusted for Gemini
                if len(parts) >= 3: # Expecting at least name, date, availability
                    event_name = parts[0].strip()
                    event_date = parts[1].strip()
                    availability = parts[2].strip()
                    events.append({
                        "name": event_name,
                        "date": event_date,
                        "availability": availability
                    })
        return events


    def _execute_show_bookings(self, statement):
        try:
            sql = "SELECT BookingReference, TicketType, EventName, Date, Quantity, Status, PaymentMethod FROM Bookings"
            self.cursor.execute(sql)
            rows = self.cursor.fetchall() # Fetch all rows from the query

            if not rows:
                print("No bookings in history.")
                output_handler("No bookings in history.")
            else:
                print("Booking History:")
                output_handler("Booking History:")
                for row in rows:
                    print(f"  Reference: {row['BookingReference']}") # Access columns by dictionary key
                    print(f"  Type:      {row['TicketType']}")
                    print(f"  Event:     {row['EventName']}")
                    print(f"  Date:      {row['Date']}")
                    print(f"  Quantity:  {row['Quantity']}")
                    print(f"  Status:    {row['Status']}")
                    if row['PaymentMethod']: # Check if PaymentMethod is not None
                        print(f"  Payment:   {row['PaymentMethod']}")
                    print("-" * 20)
                    
                    output_handler(f"  Reference: {row['BookingReference']}") # Access columns by dictionary key
                    output_handler(f"  Type:      {row['TicketType']}")
                    output_handler(f"  Event:     {row['EventName']}")
                    output_handler(f"  Date:      {row['Date']}")
                    output_handler(f"  Quantity:  {row['Quantity']}")
                    output_handler(f"  Status:    {row['Status']}")
                    if row['PaymentMethod']: # Check if PaymentMethod is not None
                        output_handler(f"  Payment:   {row['PaymentMethod']}")
                    output_handler("-" * 20)
        except mysql.connector.Error as ex:
            print(f"Database error showing bookings: {ex}")
            output_handler(f"Database error showing bookings: {ex}")

    def __del__(self): # Destructor to close connection when Interpreter object is deleted
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
            output_handler("Database connection closed.")
