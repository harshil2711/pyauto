# Add to cart button click
element = await page.querySelector('#product-addtocart-button')
await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
await element.click()

+++++++++++++++++++++++++

# View cart button to be present and visible with increased timeout and error handling
        try:
            element = await page.waitForSelector('a.action.viewcart[data-id="view_cart"]', {'visible': True, 'timeout': 30000})
            await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
            await asyncio.sleep(2)  # Small delay after scroll
            await element.click()
            print("✅ Successfully clicked view cart button")
        except Exception as e:
            print(f"⚠️ Failed to click view cart button: {str(e)}")
            # Try alternative approach if first attempt fails
            try:
                await page.evaluate('document.querySelector(\'a.action.viewcart[data-id="view_cart"]\').click()')
                print("✅ Used alternative method to click view cart button")
            except Exception as e2:
                print(f"⚠️ Both methods failed to click view cart button: {str(e2)}")

_________________________________________________________

# Click the Priority shipping method with improved error handling
        try:
            # Try multiple approaches to select shipping method with longer timeout
            selectors = [
                'label[for*="priority"]'  # Try clicking label directly
            ]
            
            for selector in selectors:
                try:
                    element = await page.waitForSelector(selector, {'visible': True, 'timeout': 15000})
                    await page.evaluate('(element) => { element.scrollIntoView({ behavior: "smooth", block: "center" }); }', element)
                    await asyncio.sleep(2)
                    
                    # Click the element once
                    try:
                        await element.click()
                    except Exception as click_err:
                        print(f"⚠️ Click attempt failed, trying alternative: {str(click_err)}")
                        await page.mouse.click(element.x, element.y)
                    
                    await asyncio.sleep(1)
                    
                    # Verify selection
                    # is_checked = await page.evaluate('(element) => element.checked', element)
                    # if not is_checked:
                    #     has_selected = await page.evaluate('(element) => element.classList.contains("selected") || element.hasAttribute("checked")', element)
                    #     if has_selected:
                    #         is_checked = True
                    
                    # if is_checked:
                    #     print(f"✅ Successfully selected shipping method using selector: {selector}")
                    #     break
                        
                except Exception as e:
                    print(f"⚠️ Attempt with selector '{selector}' failed: {str(e)}")
                    continue
            else:
                pass
                
        except Exception as e:
            print(f"⚠️ Failed to select shipping method: {str(e)}")
    



