"use strict";
/*jslint todo: true, regexp: true, browser: true, unparam: true, plusplus: true */
/*global Promise */
var jQuery = require('jquery/dist/jquery.slim.js');
var api = require('./api.js');

function escapeHTML(s) {
    return new Option(s).innerHTML;
}

function renderSubsetInfo(si) {
    if (!si) {
        return "";
    }

    return Object.keys(si).map(function (k) {
        return {
            all: "",
            shortsus: "Short Suspensions: ",
            longsus: "Long suspensions: ",
            quote: "Quotes: ",
            nonquote: "Non-quotes: ",
        }[k] + si[k] + (si[k] > 1 ? " words" : " word");
    }).join(", ");
}

function renderChapters(items) {
    return items.map(function (i) {
        return '<a href="/chapter?chapter_id=' + i.id + '" title="' + renderSubsetInfo(i.subset_info) + '">' + escapeHTML(i.title) + "</a>";
    }).join(", ");
}

function renderBooks(items) {
    return items.map(function (i) {
        return "<h4>" + escapeHTML(i.title) + " (" + escapeHTML(i.author) + "): <small>" + renderSubsetInfo(i.subset_info) + "</small></h3>" +
            renderChapters(i.children || []);
    }).join("\n");
}

function renderCorpora(items) {
    return items.map(function (i) {
        return '<h3 id="' + escapeHTML(i.id) + '">' + escapeHTML(i.title) + ": <small>" + renderSubsetInfo(i.subset_info) + "</small></h2>" +
            renderBooks(i.children || []);
    }).join("\n");
}

function renderCorporaHeadings(items) {
    return "<ul>" + items.map(function (i) {
        return '<li><a href="#' + escapeHTML(i.id) + '">' + escapeHTML(i.title) + "</a></li>";
    }).join("\n") + "</ul>";
}

function PageContents(content_el) {
    this.content_el = content_el;
}

PageContents.prototype.reload = function reload(page_state) {
    var self = this;

    return api.get('corpora/details').then(function (details) {
        self.content_el.innerHTML =
            '<div class="clic-contents">' +
            '<p>Welcome to CLiC. The CLiC web app has been developed as part of the <a href="https://www.birmingham.ac.uk/schools/edacs/departments/englishlanguage/research/projects/clic/index.aspx">CLiC Dickens project</a>, ' +
            'which demonstrates through corpus stylistics how computer-assisted methods can be used to study literary texts and lead to new insights into how readers perceive fictional characters.</p>' +
            '<p>Please choose a function in the control bar to the right (click the icon in the top right if it is not displayed).</p>' +
            '<p>CLiC currently contains the following texts:</p><div>' +
            renderCorporaHeadings(details.corpora) +
            renderCorpora(details.corpora) +
            '</div></div>';
    });

};

module.exports = PageContents;
