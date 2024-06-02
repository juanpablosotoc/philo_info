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
