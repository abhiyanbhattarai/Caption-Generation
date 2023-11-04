# Caption-Generation
- This project is a web based application that allows users to upload images and generate captions for those images. 
- Users can edit the generated caption and post that image and caption to social media(IG).
- It utilizes a pre-trained deep learning model for image captioning and a Flask-based user interface to make it accessible through a web browser.

## How To Run?

- First, make sure to create and activate a virtual environment:
      ```bash
      python -m venv venv_name  # Create a virtual environment
      ```
      ```bash
      source venv_name/bin/activate  # Activate the virtual environment (for macOS/Linux)
      ```

      ```bash
      venv_name\Scripts\activate  # Activate the virtual environment (for Windows) 
      ```     

1. Install Requirements.txt

    ```bash 
    pip install -r Requirements.txt
    ```
2. Download Spacy Data Model.

      ```bash
      python -m spacy download en
      ```

3. Run the app.

      ```bash
      python main.py
      ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## ScreenShots

#### Home Page
![Home Page](Homepage.PNG)