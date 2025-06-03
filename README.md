# Library Management System 📚

A simple console-based Library Management System built with Python and SQLite.

## ✨ Features

- 📖 **Books Management**
  - Add, list, search, update, and delete books
  - Manage number of copies for each book

- 👥 **Patrons Management**
  - Add, list, search, update, and delete patrons
  - Unique email constraint for patrons

- 🔄 **Borrowing System**
  - Borrow books (only if copies are available)
  - Return books and update records
  - View full borrow/return history

## 🗂 Database Schema

- **Books**
  - `id`: Auto-increment primary key
  - `title`, `author`, `year`, `copies`

- **Patrons**
  - `id`: Auto-increment primary key
  - `name`, `email` (unique)

- **BorrowRecords**
  - `id`: Auto-increment primary key
  - `book_id`, `patron_id`
  - `borrow_date`, `return_date`

## 🚀 Getting Started

### Requirements

- Python 3.x

### How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/library-management-system.git
   cd library-management-system
