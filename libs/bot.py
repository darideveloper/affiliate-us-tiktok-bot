from time import sleep
from libs.web_scraping import WebScraping


class Bot(WebScraping):
    
    def __init__(self, chrome_folder: str, creators_num_loop: int):
        """ Start chrome and load home page
        
        Args:
            chrome_folder (str): path to chrome data folder
            creators_num_loop (int): number of loops to save creators
        """
        
        # Save settings
        self.creators_num_loop = creators_num_loop
        
        # Start chrome
        super().__init__(
            chrome_folder=chrome_folder,
            start_killing=True
        )
        
        # Load home page
        self.home_page = "https://affiliate-us.tiktok.com/" \
            "connection/creator?shop_region=US"
        self.set_page(self.home_page)
        
        self.refresh_selenium(time_units=2)
    
    def __select_dropdown__(self, selector_dropdown: str, elem_text: str):
        """ Select specific drop down element
        
        Args:
            selector_dropdown (str): selector for dropdown
            elem_text (str): text of element to select
        """
        
        selectors = {
            "options": 'li > label + *',
            "input": 'li:nth-child(index) > label > input'
        }
        
        # Display dropdown options
        self.click(selector_dropdown)
        self.refresh_selenium()
        
        # Select specific option
        option_found = False
        options = self.get_elems(selectors["options"])
        for option in options:
            if option.text == elem_text:
                option_index = options.index(option)
                selector_input = selectors["input"].replace(
                    "index",
                    str(option_index + 1)
                )
                self.click_js(selector_input)
                option_found = True
                break
        return option_found
    
    def login(self):
        """ Validate correct login and close popups
        """
        
        selectors = {
            "profile_image": '.m4b-avatar-image img',
        }
        image_elem = self.get_elem(selectors["profile_image"])
        if not image_elem:
            return False
        
        return True
    
    def filter_creators(self, category: str, followers: str,
                        content_type: str, creator_agency: str):
        """ Apply filters to search creators
        
        Args:
            category (str): category to filter
            followers (str): followers range to filter (as text)
            content_type (str): content type to filter
            creator_agency (str): creator agency to filter
        """
        
        selectors = {
            "creators_btn": '.m4b-dropdown + .arco-spin.w-full button',
            "categories": '#categories > div > button',
            "followers": '#followerSize > div > button',
            "content_type": '#contentType > div > button',
            "creator_agency": '#creatorAgency > div > button',
        }
        
        self.click(selectors["creators_btn"])
        self.refresh_selenium()
        self.__select_dropdown__(selectors["categories"], category)
        self.__select_dropdown__(selectors["followers"], followers)
        self.__select_dropdown__(selectors["content_type"], content_type)
        self.__select_dropdown__(selectors["creator_agency"], creator_agency)
    
    def save_creators(self):
        """ Save new creators """
               
        selectors = {
            "row": '.arco-table-body tr',
            "separator": '.arco-table-body tr + div',
            'save_btn': 'td:last-child button:nth-child(2)',
            'svg_selector_saved': '.alliance-icon.alliance-icon-Saved'
        }
        
        creators_saved = 0
        while True:
        
            # Remove separator
            script = f"""document.querySelectorAll('{selectors['separator']}')
                        .forEach(div => div.remove())"""
            self.driver.execute_script(script)
            self.refresh_selenium()
            
            # Click in "save" buttons
            rows_elems = self.get_elems(selectors["row"])
            for row_index in range(len(rows_elems)):
                            
                # Generate selector
                save_selector = f"{selectors['row']}:nth-child({row_index + 1})"
                save_selector += f" {selectors['save_btn']}"
                
                # Validate if creator is already saved
                selector_svg = f"{save_selector} {selectors['svg_selector_saved']}"
                svg_elem = self.get_elems(selector_svg)
                if svg_elem:
                    continue
                self.click_js(save_selector)
                sleep(4)
                
                # Increase counter and end loop when reach limit
                creators_saved += 1
                if creators_saved >= self.creators_num_loop:
                    return
                
            # Load more creators
            self.go_bottom()
            self.refresh_selenium(time_units=3)
                            
    def show_saved_creators(self):
        pass
    
    def invtate_creators(self):
        pass
    
    def send_invitation(self):
        pass
