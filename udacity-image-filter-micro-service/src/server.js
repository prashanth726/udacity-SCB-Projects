const express = require("express");
const bodyParser = require("body-parser");
const validUrl = require("valid-url");
const onFinished = require("on-finished");
const { filterImageFromURL, deleteLocalFiles } = require("./util/util");

(async () => {
  // Init the Express application
  const app = express();

  // Set the network port
  const port = process.env.PORT || 8082;

  // Use the body parser middleware for post requests
  app.use(bodyParser.json());

  // @TODO1 IMPLEMENT A RESTFUL ENDPOINT
  // GET /filteredimage?image_url={{URL}}
  // endpoint to filter an image from a public url.
  // IT SHOULD
  //    1
  //    1. validate the image_url query
  //    2. call filterImageFromURL(image_url) to filter the image
  //    3. send the resulting file in the response
  //    4. deletes any files on the server on finish of the response
  // QUERY PARAMATERS
  //    image_url: URL of a publicly accessible image
  // RETURNS
  //   the filtered image file [!!TIP res.sendFile(filteredpath); might be useful]

  /**************************************************************************** */

  //! END @TODO1

  // Root Endpoint
  // Displays a simple message to the user
  app.get("/filteredimage", async (req, res) => {
    const image_url = req.query.image_url;
    //validate the image URL
    if (validUrl.isUri(image_url)) {
      filterImageFromURL(image_url)
        .then((filteredpath) => {
          res.sendFile(filteredpath);
          //deletes any files on the server on finish of the response with onFinished package
          onFinished(res, function () {
            deleteLocalFiles([filteredpath]);
          });
        })
        .catch((error) => {
          console.log("error: ", error);
          res.status(422).send("The image URL is not valid");
        });
    } else {
      res.status(422).send("The image URL is not valid");
    }
  });

  app.get("/", async (req, res) => {
    res.send("try GET /filteredimage?image_url={{}}");
  });

  // Start the Server
  app.listen(port, () => {
    console.log(`server running http://localhost:${port}`);
    console.log(`press CTRL+C to stop server`);
  });
})();
