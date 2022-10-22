class Link {
    constructor(text, link) {
        this.text = text;
        this.link = link;
    }
}

class LinkTreeNode {
    constructor(link) {
        this.link = link;
        this.descendants = [];
    }
}


