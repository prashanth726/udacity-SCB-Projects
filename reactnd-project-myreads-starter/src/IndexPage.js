import React from "react";
import * as BooksAPI from "./BooksAPI";
import "./App.css";
import BookItem from "./components/BookItem";
import ListBook from "./components/ListBook";
import toast from "react-hot-toast";

class IndexPage extends React.Component {
  state = {
    books: {},
    searchResults: [],
    isSeachOn: false,
    error: false,
  };

  getBooksFromApi = () => {
    return BooksAPI.getAll().then((data) => {
      // Group the books based on Shelf Category
      const books = data.reduce(function(previousValue, currentValue) {
        previousValue[currentValue.shelf] =
          previousValue[currentValue.shelf] || [];
        previousValue[currentValue.shelf].push(currentValue);
        return previousValue;
      }, {});
      return books;
    });
  };

  componentDidMount() {
    this.getBooksFromApi().then((books) => {
      this.setState({ books: books });
    });
  }

  updateBooksFromApi = () => {
    toast.loading("Updating", {
      position: "bottom-top",
    });
    this.getBooksFromApi().then((books) => {
      this.setState({ books: books });
    });
  };

  render() {
    const state = this.state;
    return (
      <div className="app">
        <div className="list-books">
          <div className="list-books-title">
            <h1>MyReads</h1>
          </div>
          <div className="list-books-content">
            {state && state.books && Object.keys(state.books).length > 0 ? (
              <ListBook
                books={state.books}
                updateBooksFromApi={this.updateBooksFromApi}
              />
            ) : (
              "Loading.. please wait"
            )}
          </div>
          <div className="open-search">
            <button onClick={() => this.props.history.push("/search")}>
              Add a book
            </button>
          </div>
        </div>
      </div>
    );
  }
}

export default IndexPage;
