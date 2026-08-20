#my sql conncetor to python(very imp)
#import mysql.connector

'''from sql_connection import get_sql_connection
def get_all_products(connection):

    
    cursor = connection.cursor()

    query = """
    SELECT
        products.product_id,
        products.name,
        products.uom_id,
        products.price_per_unit,
        uom.uom_name
    FROM products
    INNER JOIN uom
        ON products.uom_id = uom.uom_id;
    """

    cursor.execute(query)

    response = []

    for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
        response.append({
            "product_id": product_id,
            "name": name,
            "uom_id": uom_id,
            "price_per_unit": price_per_unit,
            "uom_name": uom_name
        })

    #cursor.close()
    #connection.close()

    return response
def insert_new_product(connection,product):
    cursor = connection.cursor()

    query = """
    INSERT INTO products (name, uom_id, price_per_unit)
    VALUES (%s, %s, %s);
    """
    data = (product['name'], product['uom_id'], product['price_per_unit'])
    cursor.execute(query, data)


    connection.commit()

    return cursor.lastrowid


def delete_product(connection,product_id):
    cursor = connection.cursor()

    query = """
    DELETE FROM products
    WHERE product_id = %s;
    """
    data = (product_id,)
    cursor.execute(query, data)

    connection.commit()

    return cursor.rowcount


def update_product(connection,product_id,product):
    cursor = connection.cursor()

    query = """
    UPDATE products
    SET name = %s, uom_id = %s, price_per_unit = %s
    WHERE product_id = %s;
    """
    data = (product['name'], product['uom_id'], product['price_per_unit'], product_id)
    cursor.execute(query, data)

    connection.commit()

    return cursor.rowcount



if __name__ == "__main__":
    connection = get_sql_connection()
    print(insert_new_product(connection, {
        "name": "Test Product",
        "uom_id": 1,
        "price_per_unit": 10.0
    }))
    #print(delete_product(connection, 15))
    print(update_product(connection, 14, {
        "name": "Updated_cabbage",
        "uom_id": 2,
        "price_per_unit": 20.0
    }))'''



from sql_connection import get_sql_connection


def get_all_products(connection):

    cursor = connection.cursor()

    query = """
    SELECT
        products.product_id,
        products.name,
        products.uom_id,
        products.price_per_unit,
        uom.uom_name
    FROM products
    INNER JOIN uom
        ON products.uom_id = uom.uom_id;

        where products.is_active = 1;
    """

    cursor.execute(query)

    response = []

    for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
        response.append({
            "product_id": product_id,
            "name": name,
            "uom_id": uom_id,
            "price_per_unit": price_per_unit,
            "uom_name": uom_name
        })

    cursor.close()

    return response


def insert_new_product(connection, product):

    cursor = connection.cursor()

    # First find uom_id using uom_name
    uom_query = """
    SELECT uom_id
    FROM uom
    WHERE uom_name = %s;
    """

    cursor.execute(uom_query, (product['unit'],))

    result = cursor.fetchone()

    if result is None:
        cursor.close()
        raise ValueError("Invalid unit: " + product['unit'])

    uom_id = result[0]

    # Insert product
    query = """
    INSERT INTO products
    (name, uom_id, price_per_unit)
    VALUES (%s, %s, %s);
    """

    data = (
        product['name'],
        uom_id,
        product['price_per_unit']
    )

    cursor.execute(query, data)

    connection.commit()

    product_id = cursor.lastrowid

    cursor.close()

    return product_id


def delete_product(connection, product_id):

    cursor = connection.cursor()

    query = """
    UPDATE products
    SET is_active = 0
    WHERE product_id = %s;
    """

    cursor.execute(query, (product_id,))

    connection.commit()

    result = cursor.rowcount

    cursor.close()

    return result


def update_product(connection, product_id, product):

    cursor = connection.cursor()

    # Find uom_id
    uom_query = """
    SELECT uom_id
    FROM uom
    WHERE uom_name = %s;
    """

    cursor.execute(uom_query, (product['unit'],))

    result = cursor.fetchone()

    if result is None:
        cursor.close()
        raise ValueError("Invalid unit: " + product['unit'])

    uom_id = result[0]

    query = """
    UPDATE products
    SET
        name = %s,
        uom_id = %s,
        price_per_unit = %s
    WHERE product_id = %s;
    """

    data = (
        product['name'],
        uom_id,
        product['price_per_unit'],
        product_id
    )

    cursor.execute(query, data)

    connection.commit()

    updated = cursor.rowcount

    cursor.close()

    return updated


if __name__ == "__main__":

    connection = get_sql_connection()

    print(
        insert_new_product(
            connection,
            {
                "name": "Test Product",
                "unit": "kg",
                "price_per_unit": 10.0
            }
        )
    )

    connection.close()