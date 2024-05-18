## [LibroTrack API](https://librotrackapi.onrender.com/api/)
* ### [PostMan Documentaion](https://documenter.getpostman.com/view/22007181/2sA3JT4eFY)
LibroTrack API is a robust solution designed to streamline library operations. It provides endpoints for librarians to manage book inventories, member information, and transactions. The API allows for efficient tracking of book quantities, issuing books to members, processing returns, and charging fees.

### Authentication

#### POST /api/login
Endpoint to authenticate users.

### Books

#### POST /api/books/
Endpoint to create a new book.

#### GET /api/books
Endpoint to retrieve all books.

#### GET /api/books/{book_id}
Endpoint to retrieve a specific book.

#### PUT /api/books/{book_id}/
Endpoint to update a specific book.

#### DELETE /api/books/{book_id}/
Endpoint to delete a specific book.

### Members

#### POST /api/members/
Endpoint to create a new member.

#### GET /api/members
Endpoint to retrieve all members.

#### GET /api/members/{member_id}
Endpoint to retrieve a specific member.

#### PUT /api/members/{member_id}/
Endpoint to update a specific member.

#### DELETE /api/members/{member_id}/
Endpoint to delete a specific member.

### Transactions

#### POST /api/transactions/
Endpoint to create a new transaction.

#### GET /api/transactions
Endpoint to retrieve all transactions.

#### GET /api/transactions/{transaction_id}
Endpoint to retrieve a specific transaction.

#### PUT /api/transactions/{transaction_id}/
Endpoint to update a specific transaction.

#### DELETE /api/transactions/{transaction_id}/
Endpoint to delete a specific transaction.

