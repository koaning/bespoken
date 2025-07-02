"""Playwright browser tool for dynamic web interaction."""

from typing import Optional
import llm

from .. import config
from playwright.sync_api import sync_playwright, Browser, Page


class PlaywrightTool(llm.Toolbox):
    """Tool for browser automation using Playwright.
    
    This tool requires the 'browser' extra to be installed:
        pip install bespoken[browser]
    """
    
    def __init__(self, headless: bool = False, browser_type: str = "chromium"):
        self.headless = headless
        self.browser_type = browser_type
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._page: Optional[Page] = None
    
    def _ensure_browser(self):
        """Ensure browser is started."""
        if self._playwright is None:
            self._playwright = sync_playwright().start()
            
        if self._browser is None:
            browser_func = getattr(self._playwright, self.browser_type)
            self._browser = browser_func.launch(headless=self.headless)
            
        if self._page is None:
            self._page = self._browser.new_page()
    
    def _debug_return(self, value: str) -> str:
        """Helper to show what the LLM receives from tools"""
        config.tool_debug(f"\n>>> Tool returning to LLM: {repr(value[:200])}...\n")
        return value
    
    def navigate(self, url: str) -> str:
        """Navigate to a URL and wait for page to load.
        
        Args:
            url: The URL to navigate to
            
        Returns:
            Success message with page title
        """
        config.tool_debug(f">>> LLM calling tool: navigate(url={repr(url)})")
        config.tool_status(f"Navigating to: {url}")
        
        self._ensure_browser()
        self._page.goto(url, wait_until="networkidle")
        title = self._page.title()
        
        config.tool_success(f"Navigated to page: {title}")
        return self._debug_return(f"Successfully navigated to {url}. Page title: {title}")
    
    def click_text(self, text: str) -> str:
        """Click an element containing specific text.
        
        Args:
            text: The visible text to click (e.g., "Submit", "Next Page")
            
        Returns:
            Success or error message
        """
        config.tool_debug(f">>> LLM calling tool: click_text(text={repr(text)})")
        config.tool_status(f"Clicking text: {text}")
        
        self._ensure_browser()
        try:
            # Use force click as primary strategy
            config.tool_debug("Using force click strategy")
            self._page.get_by_text(text).first.click(force=True)
            
            config.tool_success(f"Clicked: {text}")
            return self._debug_return(f"Successfully clicked element with text: {text}")
        except Exception as e:
            error_msg = f"Failed to click text '{text}': {str(e)}"
            config.tool_error(error_msg)
            return self._debug_return(f"Error: {error_msg}")
    
    def fill_field(self, label_or_placeholder: str, text: str) -> str:
        """Fill a text input field by its label or placeholder text.
        
        Args:
            label_or_placeholder: The label text or placeholder text of the input
            text: Text to fill in
            
        Returns:
            Success or error message
        """
        config.tool_debug(f">>> LLM calling tool: fill_field(label_or_placeholder={repr(label_or_placeholder)}, text={repr(text)})")
        config.tool_status(f"Filling field: {label_or_placeholder}")
        
        self._ensure_browser()
        try:
            # Try by label first
            try:
                self._page.get_by_label(label_or_placeholder).fill(text)
            except:
                # Try by placeholder
                self._page.get_by_placeholder(label_or_placeholder).fill(text)
            
            config.tool_success(f"Filled {label_or_placeholder} with text")
            return self._debug_return(f"Successfully filled field '{label_or_placeholder}' with: {text}")
        except Exception as e:
            error_msg = f"Failed to fill field '{label_or_placeholder}': {str(e)}"
            config.tool_error(error_msg)
            return self._debug_return(f"Error: {error_msg}")
    
    def get_content(self) -> str:
        """Get the current page content as text.
        
        Returns:
            The visible text content of the page
        """
        config.tool_debug(">>> LLM calling tool: get_content()")
        config.tool_status("Getting page content")
        
        self._ensure_browser()
        try:
            # Get all visible text
            content = self._page.inner_text("body")
            
            # Truncate if too long
            if len(content) > 50000:
                content = content[:50000] + "\n... (truncated)"
            
            config.tool_success(f"Retrieved {len(content):,} characters of content")
            return self._debug_return(content)
        except Exception as e:
            error_msg = f"Failed to get content: {str(e)}"
            config.tool_error(error_msg)
            return self._debug_return(f"Error: {error_msg}")
    
    def screenshot(self, path: str = "screenshot.png") -> str:
        """Take a screenshot of the current page.
        
        Args:
            path: Path to save the screenshot
            
        Returns:
            Success message with file path
        """
        config.tool_debug(f">>> LLM calling tool: screenshot(path={repr(path)})")
        config.tool_status(f"Taking screenshot: {path}")
        
        self._ensure_browser()
        try:
            self._page.screenshot(path=path)
            config.tool_success(f"Screenshot saved: {path}")
            return self._debug_return(f"Screenshot saved to: {path}")
        except Exception as e:
            error_msg = f"Failed to take screenshot: {str(e)}"
            config.tool_error(error_msg)
            return self._debug_return(f"Error: {error_msg}")
    
    def wait_for_text(self, text: str, timeout: int = 30000) -> str:
        """Wait for specific text to appear on the page.
        
        Args:
            text: Text to wait for
            timeout: Maximum wait time in milliseconds
            
        Returns:
            Success or timeout message
        """
        config.tool_debug(f">>> LLM calling tool: wait_for_text(text={repr(text)}, timeout={timeout})")
        config.tool_status(f"Waiting for text: {text}")
        
        self._ensure_browser()
        try:
            self._page.get_by_text(text).wait_for(timeout=timeout)
            config.tool_success(f"Text appeared: {text}")
            return self._debug_return(f"Text '{text}' is now visible on the page")
        except Exception as e:
            error_msg = f"Timeout waiting for text '{text}': {str(e)}"
            config.tool_error(error_msg)
            return self._debug_return(f"Error: {error_msg}")
    
    def close(self) -> str:
        """Close the browser and clean up resources."""
        config.tool_debug(">>> LLM calling tool: close()")
        config.tool_status("Closing browser")
        
        try:
            if self._page:
                self._page.close()
                self._page = None
            if self._browser:
                self._browser.close()
                self._browser = None
            if self._playwright:
                self._playwright.stop()
                self._playwright = None
            
            config.tool_success("Browser closed")
            return self._debug_return("Browser closed successfully")
        except Exception as e:
            error_msg = f"Error closing browser: {str(e)}"
            config.tool_error(error_msg)
            return self._debug_return(f"Error: {error_msg}")
    
    def __del__(self):
        """Cleanup on deletion."""
        if self._browser:
            self.close()