#!/usr/bin/python3
import seed


def stream_user_ages():
    """
    Generator that yields user ages one by one from the DB.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:   # first loop
        yield row["age"]
    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Calculate average age of users using the generator.
    No SQL AVG, only iteration with yield.
    """
    total_age = 0
    count = 0
    for age in stream_user_ages():  # second loop
        total_age += age
        count += 1

    if count == 0:
        return 0
    return total_age / count


if __name__ == "__main__":
    avg = calculate_average_age()
    print(f"Average age of users: {avg}")
