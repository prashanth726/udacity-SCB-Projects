import React from "react";
import * as BooksAPI from "../BooksAPI";
import "../App.css";


import BookItem from "./BookItem";

class ListBook extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const books = this.props.books;

    return (
      <div>
        <div className="bookshelf">
          <h2 className="bookshelf-title">currentlyReading</h2>
          <div className="bookshelf-books">
            <ol className="books-grid">
              {books && books["currentlyReading"] ? (
                books["currentlyReading"].map((book) => (
                  <div>
                    {" "}
                    <BookItem
                      book={book}
                      updateBooksFromApi={this.props.updateBooksFromApi}
                    />
                  </div>
                ))
              ) : (
                <div>No Books Found in this shelf</div>
              )}
            </ol>
          </div>
          <h2 className="bookshelf-title">read</h2>
          <div className="bookshelf-books">
            <ol className="books-grid">
              {books && books["read"] ? (
                books["read"].map((book) => (
                  <div>
                    {" "}
                    <BookItem
                      book={book}
                      updateBooksFromApi={this.props.updateBooksFromApi}
                    />
                  </div>
                ))
              ) : (
                <div>No Books Found in this shelf</div>
              )}
            </ol>
          </div>
          <h2 className="bookshelf-title">wantToRead</h2>
          <div className="bookshelf-books">
            <ol className="books-grid">
              {books && books["wantToRead"] ? (
                books["wantToRead"].map((book) => (
                  <div>
                    {" "}
                    <BookItem
                      book={book}
                      updateBooksFromApi={this.props.updateBooksFromApi}
                    />
                  </div>
                ))
              ) : (
                <div>No Books Found in this shelf</div>
              )}
            </ol>
          </div>
        </div>
      </div>
    );
  }
}

export default ListBook;
