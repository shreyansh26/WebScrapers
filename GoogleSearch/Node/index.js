const puppeteer = require('puppeteer')

async function run() {
  const browser = await puppeteer.launch({
    headless: true
  });

  const page = await browser.newPage();

  await page.goto('https://www.google.com');
  await page.screenshot({ path: 'screenshots/google.png'});

  const INPUT_SELECTOR = '#lst-ib';
  const BUTTON_SELECTOR = '#tsf > div.tsf-p > div.jsb > center > input[type="submit"]:nth-child(1)';

  await page.click(INPUT_SELECTOR);
  await page.keyboard.type('Sachin Tendulkar');

  await page.click(BUTTON_SELECTOR);

  await page.waitForNavigation();
  await page.screenshot({ path: 'screenshots/sachin.png'});
  //const SEARCH_RESULTS_SELECTOR = '#rso > div:nth-child(3) > div > div:nth-child(INDEX) > div > div > h3 > a';
  const SEARCH_RESULTS_SELECTOR = 'h3.r > a';
  const LIST_CLASS = 'r';

  let listLength = await page.evaluate((sel) => {
    return document.getElementsByClassName(sel).length;
  }, LIST_CLASS);

  console.log(listLength);

  let search_result = await page.evaluate((sel) => {
    let result =  document.querySelectorAll(sel);
    return result;
  }, SEARCH_RESULTS_SELECTOR)
  .catch(error => console.log('Error1!'));
  if(!search_result)
    console.log('Error2!')

  let len = Object.keys(search_result).length;
  for (let i=0; i<len; i++) {
    //console.log(search_result[i].href);
    console.log(search_result[i].getAttribute('href'));
  }
}

run();
