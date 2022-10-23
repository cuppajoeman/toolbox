// Create a "close" button and append it to each list item
let myNodelist = document.getElementsByTagName("LI");
for (let i = 0; i < myNodelist.length; i++) {
    let span = document.createElement("SPAN");
    let txt = document.createTextNode("\u00D7");
    span.className = "close";
    span.appendChild(txt);
    myNodelist[i].appendChild(span);
}

// Click on a close button to hide the current list item
let close = document.getElementsByClassName("close");
for (let i = 0; i < close.length; i++) {
    close[i].onclick = function() {
        let div = this.parentElement;
        div.style.display = "none";
    }
}

// Add a "checked" symbol when clicking on a list item
let list = document.querySelector('ul');
list.addEventListener('click', function(ev) {
    if (ev.target.tagName === 'LI') {
        let active = ev.target.classList.contains('active');
        let checked = ev.target.classList.contains('checked');
        let start_time_element = ev.target.childNodes[ev.target.childNodes.length - 1];

        if (!active && !checked) {
            ev.target.classList.add('active');

            let today = new Date();
            let n = today.toLocaleTimeString();
            start_time_element.innerHTML = 'started at: ' + n;

        } else if(active && !checked) {
            ev.target.classList.remove('active');
            ev.target.classList.add('checked');

            let today = new Date();
            let n = today.toLocaleTimeString();
            start_time_element.innerHTML = 'completed at: ' + n;

        } else if (checked) {
            ev.target.classList.remove('checked');
            start_time_element.innerHTML = '';
        }
    }
}, false);

// Create a new list item when clicking on the "Add" button
function newElement() {
    let li = document.createElement("li");
    li.setAttribute('draggable', true);
    let inputValue = document.getElementById("myInput").value;
    let t = document.createTextNode(inputValue);
    li.appendChild(t);
    if (inputValue === '') {
        alert("You must write something!");
    } else {
        document.getElementById("myUL").appendChild(li);
    }
    document.getElementById("myInput").value = "";


    let close_span = document.createElement("SPAN");
    let txt = document.createTextNode("\u00D7");
    // close_span.className = "close";
    close_span.classList.add('right_side_list_item')
    close_span.classList.add('close')
    close_span.appendChild(txt);

    let start_span = document.createElement("SPAN");
    start_span.classList.add('right_side_list_item')

    li.appendChild(close_span);
    li.appendChild(start_span);

    for (let i = 0; i < close.length; i++) {
        close[i].onclick = function() {
            let div = this.parentElement;
            div.style.display = "none";
        }
    }
}
