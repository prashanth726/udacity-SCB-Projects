import React from "react";
import * as BooksAPI from "../BooksAPI";
import toast from "react-hot-toast";
import "../App.css";

class BookItem extends React.Component {
  constructor(props) {
    super(props);
  }

  state = {
    value: this.props.book.shelf,
  };

  moveBooktoShelf = (shelf, book) => {
    // Update the select dropdown value.
    this.setState({ value: shelf });
    // Call the BooksApi to update the Shelf

    BooksAPI.update(book, shelf).then((data) => {
      this.props.updateBooksFromApi();
      toast.success("Book Shelf Changed", {
        position: "bottom-right",
      });
    });
  };

  render() {
    const book = this.props.book;
    return (
      <li>
        <div className="book">
          <div className="book-top">
            <div
              className="book-cover"
              style={{
                width: 128,
                height: 188,
                backgroundImage: `url(${book.imageLinks.thumbnail})`,
              }}
            />
            <div className="book-shelf-changer">
              <select
                value={this.state.value}
                onChange={(val) => this.moveBooktoShelf(val.target.value, book)}
              >
                <option value="move" disabled>
                  Move to...
                </option>
                <option value="currentlyReading">Currently Reading</option>
                <option value="wantToRead">Want to Read</option>
                <option value="read">Read</option>
                <option value="none">None</option>
              </select>
            </div>
          </div>
          <div className="book-title">{book.title}</div>
          {book && book.authors && book.authors.map((author) => (
            <div className="book-authors">{author}</div>
          ))}
        </div>
      </li>
    );
  }
}

export default BookItem;
