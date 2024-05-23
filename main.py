"""
This script demonstrates how to use the Google AI Python SDK to interact with the Gemini API.
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""
# Path: main.py

import os

import google.generativeai as genai


def print_introduction(name):
    print(f"Welcome to {name}!")
    print("This script demonstrates how to use the Google AI Python SDK to interact with the Gemini API.")
    print("Install the Google AI Python SDK")
    print("\n$ pip install google-generativeai\n")
    print("See the getting started guide for more information:")
    print("https://ai.google.dev/gemini-api/docs/get-started/python\n")


genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "Context : As sql specialist in postgres 12 and up you help people optimize any SQL queries and can answer any questions about DDL and SQL giving advice and explaining why your code is more efficient. you work step by step explaining and asking questions as neededto give the more useful pragmatic answers you can even give some spontaneous tips and tricks on how to optimize sql queries. \nQuestion : write DDL for storing a complete building  information, owner and address should be denormalized as needed in separate tables, pk index sould alwas be named id. you can store geometry by using postgis\n\n",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Let's design your database schema for storing building information!  Since you're using PostgreSQL "
                "12+, we can leverage its powerful features like PostGIS for geometry.\n\nBefore we start writing "
                "DDL, let's discuss your needs further to ensure an optimal design. Could you tell me:\n\n1. **What "
                "specific information do you need to store about buildings?** (e.g., number of floors, year built, "
                "building type, etc.)\n2. **Will you be storing multiple addresses per building?** (This is important "
                "for denormalization)\n3. **How will you be using the geometry data?**  (e.g., finding buildings "
                "within a certain radius, calculating distances, etc.) \n\nOnce I have a clearer picture of your "
                "requirements, I can provide you with a well-optimized and efficient schema. \n",
            ],
        },
        {
            "role": "user",
            "parts": [
                "1 :  number of appartments and floors, year build, type (enum commercial, residential,  mixt, "
                "private,rental),  name as string, city id (points to a dictionary of cities) , ground surface . \n2: "
                "yes multiple addresses by building\n3: one position geom as  2d point for quick location and other "
                "spatial queries,  and one shape geom as multi-polygon for drawing it on screen or on GIS \n",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Excellent! With this information, let's craft some efficient DDL.\n\n```sql\n-- Building Types "
                "enum\nCREATE TYPE building_type AS ENUM ('commercial', 'residential', 'mixed', 'private', "
                "'rental');\n\n-- Cities table (assuming you have a separate table for this)\n-- CREATE TABLE cities "
                "(\n--     id SERIAL PRIMARY KEY,\n--     name VARCHAR(255) UNIQUE NOT NULL\n-- );\n\n-- Addresses "
                "table \nCREATE TABLE addresses (\n    id SERIAL PRIMARY KEY,\n    building_id INT NOT NULL,"
                "\n    street VARCHAR(255) NOT NULL,\n    house_number VARCHAR(50),\n    zip_code VARCHAR(20),"
                "\n    city_id INT REFERENCES cities(id) ON DELETE CASCADE,  -- Assuming you want addresses deleted "
                "if a city is removed\n    UNIQUE (building_id, street, house_number, zip_code) -- Ensure address "
                "uniqueness per building\n);\n\n-- Buildings table\nCREATE TABLE buildings (\n    id SERIAL PRIMARY "
                "KEY,\n    name VARCHAR(255),\n    year_built INT,\n    type building_type NOT NULL,"
                "\n    num_apartments INT,\n    num_floors INT,\n    ground_surface REAL,  -- Assuming a unit like "
                "square meters\n    position GEOGRAPHY(POINT,4326), -- 4326 is the SRID for standard "
                "latitude/longitude\n    shape GEOGRAPHY(MULTIPOLYGON,4326)\n);\n\n-- Add foreign key constraint "
                "after creating both tables to avoid circular dependency\nALTER TABLE addresses ADD CONSTRAINT "
                "fk_building\nFOREIGN KEY (building_id) REFERENCES buildings(id) ON DELETE CASCADE;\n\n-- Indices ("
                "beyond the primary keys)\nCREATE INDEX building_position_idx ON buildings USING GIST ("
                "position);\nCREATE INDEX building_shape_idx ON buildings USING GIST (shape);\nCREATE INDEX "
                "address_city_id_idx ON addresses (city_id); \n```\n\n**Explanation and Optimizations:**\n\n- "
                "**Enums:** Using `building_type` as an enum enforces data integrity and saves storage compared to "
                "plain text.\n- **Cities Table:** Assuming you already have a cities table. If not, the commented-out "
                "code provides a basic structure.\n- **Denormalization:**  We're storing multiple addresses per "
                "building in the `addresses` table, linked by `building_id`. This is a denormalized approach suitable "
                "for your use case.\n- **Foreign Keys:**  Foreign key constraints maintain relational integrity. The "
                "`ON DELETE CASCADE` ensures dependent data is deleted when a building is removed (addresses in this "
                "case).\n- **Geography Type:** PostGIS's `GEOGRAPHY` type is used for both `position` and `shape`. "
                "The 4326 SRID ensures accurate spatial calculations.\n- **GIST Indices:** Essential for efficient "
                "spatial queries on the `position` and `shape` columns.\n- **Address Index:** The "
                "`address_city_id_idx` will speed up queries filtering buildings by city.\n\n**Additional "
                "Considerations:**\n\n- **Data Validation:** Consider adding constraints to enforce data validity, "
                "e.g., `CHECK` constraints for positive values in `num_apartments`, `num_floors`, "
                "and `ground_surface`.\n- **Full-Text Search:** If you need to search buildings by name or address, "
                "consider using PostgreSQL's full-text search capabilities.\n- **Concurrency:** Depending on the "
                "scale of your application, you might need to consider locking strategies to manage concurrent access "
                "to your data.\n\nLet me know if you have any other questions or would like me to elaborate on "
                "specific parts! \n",
            ],
        },
    ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)
print(chat_session.history)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_introduction('the SQL expert chatbot')
