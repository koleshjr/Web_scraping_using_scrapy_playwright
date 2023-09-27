// scroll into view and click it laoding more elenments

const interval_id = setInterval(function(){
    const button = document.querySelector('div.py-3.ng-star-inserted > button');

    if (button) {
        button.scrollIntoView();
        button.click();
    } else {
        clearInterval(interval_id);
    }
}, 1000);