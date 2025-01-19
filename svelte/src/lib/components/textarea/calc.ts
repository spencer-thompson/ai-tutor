// Dealing with Textarea Height
function calcHeight(value) {
	let numberOfLineBreaks = (value.match(/\n/g) || []).length;
	// min-height + lines x line-height + padding + border
	let newHeight = 20 + numberOfLineBreaks * 20 + 12 + 2;
	return newHeight;
}
