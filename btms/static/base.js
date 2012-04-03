//Global variable telling us whether the page has been changed
var isPageChanged = false;

window.onbeforeunload = unsavedChangesWarning;

function isKeyIn(key, array)
{
    for (var i = 0; i < array.length; i++)
    {
        if (array[i] === key)
            return i 
    }
    return -1;
}

//Find the unique date and status IDs from the input fields
function findIDs()
{
    var date_ids = [];
    var status_ids = []
    
    //Loop through the input variables, looking for IDs
    $("input[type=text]").each(function() {
        //Add to date_ids if it's not already in there
        var date = $(this).attr("id").split("_")[0];
        var status = $(this).attr("id").split("_")[1];

        if (isKeyIn(date, date_ids) === -1)
            date_ids.push(date);

        if (isKeyIn(status, status_ids) === -1)
            status_ids.push(status);
    });
    
    var value = [date_ids, status_ids]
    return value;
}

//Run through the fields and update the status and day totals
function updateTotals()
{
    var ids = findIDs();
    var date_ids = ids[0];
    var status_ids = ids[1];
    var grandTotal = 0;

    // Update the totals for each day
    for (var i = 0; i < date_ids.length; i++)
    {
        var total = 0;

        // Find all elements that start with the date ID
        $("input[id^=" + date_ids[i] + "]").each(function() {
            var value = parseFloat($(this).val());

            if (!isNaN(value))
                total += value;
        });

        $("span[id=" + date_ids[i] + "_total]").text(total);
        console.log("Setting total for " + date_ids[i] + " to " + total);
        grandTotal += total;
    }

    // Update the totals for each status
    for (var i = 0; i < status_ids.length; i++)
    {
        var total = 0;

        //Find all elements that end with the status ID
        $("input[id$=" + status_ids[i] + "]").each(function() {
            var value = parseFloat($(this).val());

            if (!isNaN(value))
                total += value;

        });

        $("span[id=" + status_ids[i] + "_total]").text(total);
    }

    $("span[id=taskNone_total]").text(grandTotal);
}

function unsavedChangesWarning(e) {
    // Only fire if the page has been changed
    if (isPageChanged)
        return "Warning: You have unsaved changes.  Are you sure you want to leave?"
}

$(document).ready(function() {
    //Set initial totals
    updateTotals();

    var textFields = $("input[type=text]");
    textFields.change(function() {isPageChanged = true; console.log("Page dirty!");});
    textFields.change(updateTotals);
});
