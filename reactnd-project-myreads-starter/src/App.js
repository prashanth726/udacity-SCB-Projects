import React from "react";
import * as BooksAPI from "./BooksAPI";
import "./App.css";
import IndexPage from "./IndexPage";
import SearchPage from "./SearchPage";
import toast from "react-hot-toast";
import { BrowserRouter, Route, Switch } from "react-router-dom";

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
      <BrowserRouter>
        <div className="app">
          <Route path="/" component={IndexPage} exact />
          <Route path="/search" component={SearchPage} />
        </div>
      </BrowserRouter>
    );
  }
}

export default BooksApp;
