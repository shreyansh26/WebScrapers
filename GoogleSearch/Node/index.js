const puppeteer = require('puppeteer')
const csv = require('csv')
const csvdata = require('csvdata')

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
  const SEARCH_RESULTS_SELECTOR = 'h3.r > a';
  const LIST_CLASS = 'r';


  let search_result_links = await page.evaluate((sel) => {
    let result =  document.querySelectorAll(sel);
    let final_result = [...result];
    links = final_result.map(link => link.href);
    titles = final_result.map(link => link.innerText)
    return [titles, links];
  }, SEARCH_RESULTS_SELECTOR)
  .catch(error => console.log('Error1!'));

  if(!search_result_links)
    console.log('Error2!')

  search_results = []
  for (let i=0; i<search_result_links[0].length; i++) {
    console.log(search_result_links[0][i] + ' -> ' + search_result_links[1][i]);
    search_results.push([i, search_result_links[0][i], search_result_links[1][i]]);
  }
  csvdata.write('./links.csv', search_results, {header: 'id,title,link'})
  browser.close()
}

run();
