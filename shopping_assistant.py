# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Shopping Assistant - AI-powered price comparison tool."""

from google import genai
from google.genai import types

from agent import BrowserAgent
from computers import Computer
from shopping_functions import save_product_info, generate_price_report, clear_product_data


class ShoppingBrowserAgent(BrowserAgent):
    """Extended BrowserAgent with shopping-specific custom functions."""

    def __init__(
        self,
        browser_computer: Computer,
        query: str,
        model_name: str,
        verbose: bool = True,
    ):
        # Initialize parent class
        super().__init__(browser_computer, query, model_name, verbose)

        # Add shopping-specific custom functions
        shopping_functions = [
            types.FunctionDeclaration.from_callable(
                client=self._client, callable=save_product_info
            ),
            types.FunctionDeclaration.from_callable(
                client=self._client, callable=generate_price_report
            ),
        ]

        # Update the tools configuration to include shopping functions
        self._generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            tools=[
                types.Tool(
                    computer_use=types.ComputerUse(
                        environment=types.Environment.ENVIRONMENT_BROWSER,
                        excluded_predefined_functions=[],
                    ),
                ),
                types.Tool(function_declarations=shopping_functions),
            ],
        )

    def handle_action(self, action: types.FunctionCall):
        """Extended handle_action to support shopping functions."""
        # Handle shopping-specific functions
        if action.name == save_product_info.__name__:
            return save_product_info(
                product_name=action.args["product_name"],
                price=action.args["price"],
                website=action.args["website"],
                url=action.args["url"],
                availability=action.args.get("availability", "Unknown")
            )
        elif action.name == generate_price_report.__name__:
            return generate_price_report(
                filename=action.args.get("filename")
            )
        else:
            # Delegate to parent class for standard actions
            return super().handle_action(action)

