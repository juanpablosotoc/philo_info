import { dateComparisonString } from "./types";

function getOffset(el: any) {
    const rect = el.getBoundingClientRect();
    return {
      left: rect.left + window.scrollX,
      top: rect.top + window.scrollY
    };
}

export function getXYPercentages(e: any, element: any) {
    const mouseX = e.pageX;
    const mouseY = e.pageY;
    const {left: cardX, top: cardY} = getOffset(element);

    const cardWidth = element.offsetWidth;
    const cardHeight = element.offsetHeight;

    const x = mouseX - cardX;
    const y = mouseY - cardY;
    const xPercent = Math.trunc((x / cardWidth) * 100);
    const yPercent = Math.trunc((y / cardHeight) * 100);

    return { xPercent, yPercent };
};

export function dateComparison( d2: Date ){
    let d1 = new Date();
    let comparison = 'Older';
    if (d1.getUTCFullYear() == d2.getUTCFullYear()) {
        comparison = 'This year';
        if (d1.getUTCMonth() == d2.getUTCMonth()) {
            comparison = 'This month';
            if (d1.getUTCDate() == d2.getUTCDate()) {
                comparison = 'Today';
            }
    }};
    return comparison as dateComparisonString;
};

export function isLink(text: string) {
    return text.startsWith('http://') || text.startsWith('https://');
};