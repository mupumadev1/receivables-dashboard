const searchBtn = document.getElementById('search-btn')
const searchDropdown = document.getElementById('search-dropdown')
const searchInput = document.getElementById('search-input')
const exportButton = document.getElementById('modal-submit-btn');
const startDateInput = document.getElementById('datepicker1');
const endDateInput = document.getElementById('datepicker2');
const datepicker1 = document.getElementById('datepicker1')
const datepicker2 = document.getElementById('datepicker2')

let numberOfPages = 0;
let hasClickedOnSearchBtn = false;
let selectedPageNumber = 1
let query_params = []


function hideModal() {
    $('#date-selector-modal').modal('hide');
}

exportButton.addEventListener('click', () => {
    if (query_params !== []) {
        const searchInput = query_params[0];
        const filterOptions = query_params[1];
        startDate = startDateInput.value
        endDate = endDateInput.value
        if (searchInput && filterOptions) {
            window.location.href = `/download?search_params=${searchInput}&filter_options=${filterOptions}&start_date=${startDate}&end_date=${endDate}`;
        }
    }

        window.location.href = `/download?start_date=${startDate}&end_date=${endDate}`;


});

searchDropdown.addEventListener('change', () => {
    searchInput.removeAttribute('readonly');

    if (searchDropdown.value === 'transaction_date' || searchDropdown.value === 'entry_date') {
        // Destroy any existing Flatpickr instance
        if (searchInput._flatpickr) {
            searchInput._flatpickr.destroy();
        }
        searchInput._flatpickr = flatpickr(searchInput, {
            dateFormat: 'Y-m-d',

        });
    } else {
        // Destroy Flatpickr if it's not the "date" option
        if (searchInput._flatpickr) {
            searchInput._flatpickr.destroy();
        }
    }
});

function handleClick(event) {
    event.preventDefault();
    const url = event.target.getAttribute('href');
    fetch(url)
        .then(response => response.text())
        .then(html => {
            updateTableAndPaginator(html)
            addEventListenerToAnchorTag();
        });
}

function updateTableAndPaginator(html) {
    const parser = new DOMParser();
    const newDoc = parser.parseFromString(html, 'text/html');

    const newTable = newDoc.getElementById('table-body');
    const newPaginator = newDoc.getElementById('paginator');
    document.getElementById('table-body').replaceWith(newTable);
    document.getElementById('paginator').replaceWith(newPaginator);
}

function addEventListenerToAnchorTag() {
    const paginationLinks = document.querySelectorAll('.custom-pagination a');
    paginationLinks.forEach(link => {
        link.addEventListener('click', handleClick); // Add the handleClick function as the event listener
    });
}

function removeEventListenerFromAnchorTag() {
    const paginationLinks = document.querySelectorAll('.custom-pagination a');
    paginationLinks.forEach(link => {
        link.removeEventListener('click', handleClick); // Remove the handleClick function as the event listener
    });
}

searchBtn.addEventListener('click', (e) => {
    e.preventDefault();
    hasClickedOnSearchBtn = true;
    query_params = [searchInput.value, searchDropdown.value];

    fetchSearchResults(query_params, selectedPageNumber);
})

function fetchSearchResults(queryParams, page) {
    const searchInput = queryParams[0];
    const filterOptions = queryParams[1];

    fetch(`search/?search_params=${searchInput}&filter_options=${filterOptions}&page=${page}`)
        .then(response => response.text())
        .then(html => {
            // Parse the HTML response
            const parser = new DOMParser();
            const newDoc = parser.parseFromString(html, 'text/html');

            const newTable = newDoc.getElementById('table-body');
            const newPaginator = newDoc.getElementById('paginator');
            numberOfPages = parseInt(newPaginator.dataset.numPages);

            const tableBody = document.getElementById('table-body');
            const paginator = document.getElementById('paginator');

            tableBody.replaceWith(newTable);
            paginator.replaceWith(newPaginator)
            updatePaginationLinks(newPaginator);
        })
        .catch(error => {
            console.error('Error fetching search results:', error);
        });
}

function updatePaginationLinks(newDoc) {
    const nextLink = newDoc.querySelector('#next')
    if (nextLink) {
        nextPageLink(nextLink)
    }
    const firstLink = newDoc.querySelector('#first')
    if (firstLink) {
        firstPageLink(firstLink)
    }
    const lastLink = newDoc.querySelector('#last')
    if (lastLink) {
        lastPageLink(lastLink)
    }
    const previousLink = newDoc.querySelector('#previous')
    if (previousLink) {
        previousPageLink(previousLink)
    }
}

async function goToPage() {

    try {
        fetchSearchResults(query_params, selectedPageNumber)
    } catch (err) {
        console.log(err);
    }
}

function nextPageLink(nextLink) {
    nextLink.addEventListener('click', (e) => {
        if (hasClickedOnSearchBtn === true) {
            e.preventDefault();
            if (selectedPageNumber !== numberOfPages) {
                selectedPageNumber += 1;
            }

            goToPage();

        }
    });
}

function previousPageLink(previousLink) {
    previousLink.addEventListener('click', (e) => {
        if (hasClickedOnSearchBtn === true) {
            e.preventDefault();
            if (selectedPageNumber !== 1) {
                selectedPageNumber -= 1;
            }

            goToPage();
        }
    });
}

function lastPageLink(lastLink) {
    lastLink.addEventListener('click', (e) => {
        if (hasClickedOnSearchBtn === true) {
            e.preventDefault();
            selectedPageNumber = numberOfPages;
            goToPage();
        }
    });
}

function firstPageLink(firstLink) {
    firstLink.addEventListener('click', (e) => {
        if (hasClickedOnSearchBtn === true) {
            e.preventDefault();
            selectedPageNumber = 1;
            goToPage();
        }
    });
}