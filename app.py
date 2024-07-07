import streamlit as st
from bs4 import BeautifulSoup
from google import generativeai as genai
import requests


page_bg_page = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://wallpapercave.com/wp/kqvP4Hn.png");
    background-size: cover;
    
}
[data-testid="stSidebarContent"] {
    background-image:url("https://media.npr.org/assets/img/2015/04/20/web_wide-1957a80d6b9a1506a0951211c3df5791cb146ade.jpg?s=1400");
    background-size: cover;
}


[class="st-emotion-cache-sh2krr e1nzilvr5"]{
    color: #ffffff; /* Text color */
    padding: 10px; /* Padding for the text */
    background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent background color */
    border-radius: 5px; /* Rounded corners */
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); /* Box shadow for depth */
}


</style>
"""
st.markdown(page_bg_page, unsafe_allow_html=True)



def normal_parse():
        
    def wtd(x):
        
        get_titleparas, get_image, get_videos, get_links = st.columns(4)

        if get_titleparas.button('Brief Overview'):
            if x == "":
                st.text("Url not found ")
            else:
                try:
                    response = requests.get(x)
                    response.raise_for_status() 
                    soup1 = BeautifulSoup(response.content, 'html.parser')
                except Exception as e:
                    st.text("Error fetching or parsing URL:", e)
                    return
                Titleandparagraph(soup1)

        if get_image.button('Get Images'):
            if x == "":
                st.text("Url not found ")
            else:
                try:
                    response = requests.get(x)
                    response.raise_for_status() 
                    soup1 = BeautifulSoup(response.content, 'html.parser')
                except Exception as e:
                    st.text("Error fetching or parsing URL:", e)
                    return
                images_parse(soup1)

        if get_videos.button('Get Videos'):
            try:
                response = requests.get(x)
                response.raise_for_status() 
                soup1 = BeautifulSoup(response.content, 'html.parser')
            except Exception as e:
                st.text("Error fetching or parsing URL:", e)
                return
            video_parse(soup1)
            
        if get_links.button('Get Links'):
            if x == "":
                st.text("Url not found ")
            else:
                try:
                    response = requests.get(x)
                    response.raise_for_status()  
                    soup1 = BeautifulSoup(response.content, 'html.parser')
                except Exception as e:
                    st.text("Error fetching or parsing URL:", e)
                    return
                link_parse(soup1)

    def mwtd(x, y):
        compare_info = st.button('Combined Research')
        
        if compare_info:
            if not x or not y:
                st.warning("Please enter valid URLs for comparison.")
                return
            
            try:
                response_x = requests.get(x)
                response_x.raise_for_status()
                soup_x = BeautifulSoup(response_x.content, 'html.parser')
            except Exception as e:
                st.error(f"Error fetching or parsing URL {x}: {e}")
                return

            try:
                response_y = requests.get(y)
                response_y.raise_for_status()
                soup_y = BeautifulSoup(response_y.content, 'html.parser')
            except Exception as e:
                st.error(f"Error fetching or parsing URL {y}: {e}")
                return

            srcx = Titleandparagraph(soup_x)
            srcy = Titleandparagraph(soup_y)
            compare_information(srcx,srcy)

    def Titleandparagraph(soup):
        """Scrapes titles and paragraphs, offering summarization or full content."""
        titles = soup.find_all('h1')  
        paragraphs = soup.find_all('p')  
        geni(titles,paragraphs)

    def geni(titles, paragraphs):
        """Generates text using GenAI based on user input, titles, and paragraphs."""
        try:
            
            generation_config = {
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }

            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
            ]

            model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                                        generation_config=generation_config,
                                        safety_settings=safety_settings)

            convo = model.start_chat(history=[])
            
            convo.send_message(f"give me a overview in {titles} and {paragraphs}")
            large_text = convo.last.text
            st.text(large_text)
            
        except Exception as e:
            return f"Error generating text: {e}"

    def images_parse(x):
        img_tags = x.find_all("img")
        image_urls = [img["src"] for img in img_tags if not img["src"].lower().endswith(".gif")]

        st.title("Images from the webpage")

        for url in image_urls:
            st.image(url, caption=url)
            
    def video_parse(x):
        video_tags = x.find_all('video')
        video_urls = [tag['src'] for tag in video_tags]
        
        if video_urls:
                st.markdown("### Videos Found:")
                for video_url in video_urls:
                    st.video(video_url)
        else:
                st.warning("No videos found on the provided URL.")

    def link_parse(x):
        link_tags = x.find_all('a', href=True)
        http_links = [tag['href'] for tag in link_tags if tag['href'].startswith('http://') or tag['href'].startswith('https://')]
        if http_links:
            st.markdown("### HTTP Links Found:")
            count = 0 
            for link in http_links:
                count += 1
                st.write(f"Link {count} : {link}")
                
        
        else:
            st.warning("No HTTP links found on the provided URL.")
            
    def compare_information(soup1, soup2):
        try:
            titles1 = soup1.find_all('h1')
            paragraphs1 = soup1.find_all('p')
            titles2 = soup2.find_all('h1')  
            paragraphs2 = soup2.find_all('p') 

            
            combined_text = f"combined smart research related to/in/within {titles1} and {titles2} with {paragraphs1} and {paragraphs2} "
            geni_output = generate_comparison_text(combined_text)

            
            st.text(geni_output)

        except Exception as e:
            st.error(f"Overloaded Information")
        
    def generate_comparison_text(text):
        try:
            
            generation_config = {
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }

            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ]

            model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                                        generation_config=generation_config,
                                        safety_settings=safety_settings)

            convo = model.start_chat(history=[])
            convo.send_message(text)
            large_text = convo.last.text
            return large_text

        except Exception as e:
            st.error(f"Error generating comparison text: {e}")
            return None
    
    st.title("Web Scrapper")

    genai.configure(api_key=" Your Api Key here ")

    url_option = st.radio("Select the number of URLs:", ("One URL", "Two URLs"))

    if url_option == "One URL":
            url1 = st.text_input("URL 1:")
            wtd(url1)

    elif url_option == "Two URLs":
            url1 = st.text_input("URL 1:")
            url2 = st.text_input("URL 2:")
            mwtd(url1,url2)

def Promptparsing():
    genai.configure(api_key=" Your Api Key here ") #-----------------------------------------------------------------------------------

    def send_message_to_gemini(message , titles ,paragraphs):
        
            
            generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
            }

            safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            ]

            model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                                        generation_config=generation_config,
                                        safety_settings=safety_settings)

            convo = model.start_chat(history=[
            ])

            convo.send_message(f"{message} related to/in/within  {titles} and {paragraphs}")
            resp = convo.last.text
            return resp

    st.title("Prompt Scraping")

    url = st.text_input("Drop Your URL to Prompt About...")
    user_input = st.text_input("What your wanna scrap!?", key="user_input")


    if url == "":
                st.text("Url not found ")
    else:
        try:
                response = requests.get(url)
                response.raise_for_status() 
                soup = BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
                st.text("Error fetching or parsing URL:", e)
        if url:
            titles = soup.find_all('h1')  
            paragraphs = soup.find_all('p') 

    if user_input :

        response = send_message_to_gemini(user_input,titles,paragraphs)
        st.markdown(f"You: {user_input}")
        st.markdown(f"Scrapy : {response}")

    if not user_input:
        st.info("Type a message in the box above to start chatting!")


selection = st.sidebar.radio("Go to", ["Parsing", "Prompt Parsing"])

if selection == "Parsing":
    normal_parse()
    
elif selection == "Prompt Parsing":
    Promptparsing()
