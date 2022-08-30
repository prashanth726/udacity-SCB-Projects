import React from "react";
import * as BooksAPI from "./BooksAPI";
import "./App.css";
import BookItem from "./components/BookItem";
import ListBook from "./components/ListBook";
import toast from "react-hot-toast";

class SearchPage extends React.Component {
  constructor(props) {
    super(props);
  }
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

  searchBook = (event) => {
    //search for the book if the input is greather than 3 letters
    if (event.target.value.length > 3) {
      this.setState({ isSeachOn: true });
      BooksAPI.search(event.target.value).then((searchResults) => {
        const error = searchResults && searchResults.hasOwnProperty("error");

        BooksAPI.getAll().then((data) => {
          let searchResultsData = [];
          if (!error) {
            searchResults.map((book) => {
              const bookShelf = data.find((x) => x.id === book.id);

              if (bookShelf) {
                searchResultsData.push({ ...book, shelf: bookShelf.shelf });
              } else {
                searchResultsData.push({ ...book, shelf: "none" });
              }
              return searchResultsData;
            });
          } else {
            searchResultsData = searchResults;
          }
          console.log("searchResultsData: ", searchResultsData);
          this.setState({
            searchResults: searchResultsData,
            isSeachOn: false,
            error: error,
          });
        });
      });
    }
    if (event.target.value.length < 3) {
      this.setState({
        searchResults: [],
        isSeachOn: false,
      });
    }
  };

  render() {
    const state = this.state;
    return (
      <div className="app">
        <div className="search-books">
          <div className="search-books-bar">
            <button
              className="close-search"
              onClick={() => this.props.history.push("/")}
            >
              Close
            </button>
            <div className="search-books-input-wrapper">
              {/*
                  NOTES: The search from BooksAPI is limited to a particular set of search terms.
                  You can find these search terms here:
                  https://github.com/udacity/reactnd-project-myreads-starter/blob/master/SEARCH_TERMS.md

                  However, remember that the BooksAPI.search method DOES search by title or author. So, don't worry if
                  you don't find a specific author or title. Every search is limited by search terms.
                */}
              <input
                onChange={this.searchBook}
                type="text"
                placeholder="Search by title or author"
              />
            </div>
          </div>
          <div className="search-books-results">
            <ol className="books-grid" />
            <div>
              {" "}
              <h1>
                {this.state.isSeachOn
                  ? "Seaching Please wait"
                  : this.state.error
                  ? "No books found with given search query"
                  : ""}
              </h1>{" "}
            </div>
            <div className="list-books">
              <div className="list-books-content">
                <ol className="books-grid">
                  {!this.state.error &&
                  this.state.searchResults &&
                  this.state.searchResults.length > 0
                    ? this.state.searchResults.map((book) => (
                        <BookItem
                          book={book}
                          updateBooksFromApi={this.updateBooksFromApi}
                        />
                      ))
                    : ""}
                </ol>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default SearchPage;
