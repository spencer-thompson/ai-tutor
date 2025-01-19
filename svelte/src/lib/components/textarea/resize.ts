export function resize(node) {
    let CR
    let ET
    const ro = new ResizeObserver((entries, observer) => {
        for (let entry of entries) {
            CR = entry.contentRect
            ET = entry.target
        }
        node.dispatchEvent(new CustomEvent('resize', {
            detail: { CR, ET }
        }));
    });
    ro.observe(node);
    return {
        destroy() {
            ro.disconnect();
        }
    }
}

// CR stands for "contentRect" which has size details of the element
// ET stands for "entry.target" which is the which is the observed DOM element

