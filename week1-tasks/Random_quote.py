from flask import Flask, request, jsonify
import sqlite3
import random

app = Flask(__name__)

Database = 'quotes.db'

def connect_db():
    return sqlite3.connect(Database)

@app.route('/quote', methods=['GET'])
def get():
    con = connect_db()
    c = con.cursor()
    c.execute('SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1')
    quote = c.fetchone()
    con.close()
    if quote:
        return jsonify({'id': quote[0], 'quote': quote[1], 'author': quote[2]})
    return jsonify({'error': 'No quotes found'}), 404

@app.route('/quotes', methods=['POST'])
def add():
    new_id = request.json.get(id)
    new_quote = request.json.get('quote')
    new_author = request.json.get('author')
    if not new_quote or not new_author:
        return jsonify({'error': 'Quote and author are required'}), 400
    
    con = connect_db()
    c = con.cursor()
    c.execute('INSERT INTO quotes (quote, author) VALUES (?, ?)', (new_quote, new_author))
    con.commit()
    con.close()
    return jsonify({'message': 'Quote added successfully'}), 201


@app.route('/quotes/<int:id>', methods=['PUT'])
def update(id):
    updated_quote = request.json.get('quote')
    updated_author = request.json.get('author')
    if not updated_quote or not updated_author:
        return jsonify({'error': 'Quote and author are required'}), 400
    
    con = connect_db()
    c = con.cursor()
    c.execute('UPDATE quotes SET quote = ?, author = ? WHERE id = ?', (updated_quote, updated_author, id))
    con.commit()
    con.close()
    return jsonify({'message': 'Quote updated successfully'}), 200


@app.route('/quotes/<int:id>', methods=['DELETE'])
def delete(id):
    con = connect_db()
    c = con.cursor()
    c.execute('DELETE FROM quotes WHERE id = ?', (id,))
    con.commit()
    con.close()
    return jsonify({'message': 'Quote deleted successfully'}), 200


@app.route('/quotes/search', methods=['GET'])
def search_byAuthor():
    author = request.args.get('author')
    if not author:
        return jsonify({'error': 'Author is required'}), 400
    
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT * FROM quotes WHERE author LIKE ?', ('%' + author + '%',))
    quotes = c.fetchall()
    conn.close()
    if quotes:
        return jsonify([{'id': q[0], 'quote': q[1], 'author': q[2]} for q in quotes])
    return jsonify({'error': 'No quotes found for the given author'}), 404

if __name__ == '__main__':
    app.run(debug=True)