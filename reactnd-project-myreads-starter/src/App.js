import React from "react";
import * as BooksAPI from "./BooksAPI";
import "./App.css";
import BookItem from "./components/BookItem";
import ListBook from "./components/ListBook";
import toast from "react-hot-toast";

class BooksApp extends React.Component {
  state = {
    books: {},
    /**
     * TODO: Instead of using this state variable to keep track of which page
     * we're on, use the URL in the browser's address bar. This will ensure that
     * users can use the browser's back and forward buttons to navigate between
     * pages, as well as provide a good URL they can bookmark and share.
     */
    showSearchPage: false,
    searchResults: [],
    isSeachOn: false,
    error: false,
  };

  getBooksFromApi = () =>{
    BooksAPI.getAll().then((data) => {
      // Group the books based on Shelf Category
      const books = data.reduce(function(previousValue, currentValue) {
        previousValue[currentValue.shelf] =
          previousValue[currentValue.shelf] || [];
        previousValue[currentValue.shelf].push(currentValue);
        return previousValue;
      }, {});
      console.log(" sjdjksbfkjesbfe")
      this.setState({ books:books });
    });
  }

  componentDidMount() {
    
    this.getBooksFromApi();
  }


  updateBooksFromApi = () => {
    toast.loading("Updating", {
      position: "bottom-top",
    });
    this.getBooksFromApi();
  };

  searchBook = (event) => {
    //search for the book if the input is greather than 3 letters
    if (event.target.value.length > 3) {
      this.setState({ isSeachOn: true });
      BooksAPI.search(event.target.value).then((searchResults) => {
        const error = searchResults && searchResults.hasOwnProperty("error");
        this.setState({
          searchResults: searchResults,
          isSeachOn: false,
          error: error,
        });
      });
    }
  };

  render() {
    console.log("re redner")
    const state = this.state;
    console.log(state.books);
    return (
      <div className="app">
        {this.state.showSearchPage ? (
          <div className="search-books">
            <div className="search-books-bar">
              <button
                className="close-search"
                onClick={() => this.setState({ showSearchPage: false })}
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
        ) : (
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
              <button onClick={() => this.setState({ showSearchPage: true })}>
                Add a book
              </button>
            </div>
          </div>
        )}
      </div>
    );
  }
}

export default BooksApp;
