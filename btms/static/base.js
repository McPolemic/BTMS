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

    // An empty timesheet has no input fields
    if (date_ids == false)
    {
        $("span[id^=date]").each(function() {
            var date = $(this).attr("id").split("_")[0];

            if (isKeyIn(date, date_ids) === -1)
                date_ids.push(date);
        })
    }
    
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

            if (value == 0)
            {
                $(this).val("");
            }

            if (!isNaN(value))
                total += value;
        });

        $("span[id=" + date_ids[i] + "_total]").text(total);
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

function addStatusRow(status_id)
{
    var ids = findIDs();
    var date_ids = ids[0];
    var status_ids = ids[1];

    // Don't add if it's already on the timesheet
    for(var i = 0; i < status_ids.length; i++)
        if (status_ids[i] === "task" + status_id)
        {
            return;
        }

    //Grab info about status
    var mytask_row = $("tr#mytask_" + status_id).children();
    var co_num = mytask_row[1].innerHTML;
    var status = mytask_row[2].innerHTML;
    var role   = mytask_row[3].innerHTML;
    var task_text;

    if (role !== "") {
        task_text = role + " - " + status;
    } else {
        task_text = status;
    }

    //Find the total line <tr> element
    var total_row = $("td:contains(Total)").parent();

    var date_fields = ""
    for (var i = 0; i < date_ids.length; i++)
    {
        date_fields += '<td class="time_entry"> \
                            <input type="text" id="' + date_ids[i] + '_task' + status_id + '" name="' + date_ids[i] + '_task' + status_id + '" /> \
                        </td>'
    }

    var row = ' <tr> \
                    <td>' + co_num + '</td> \
                    <td>' + task_text + '</td> \
                    ' + date_fields + ' \
                    <td class="align_right"><span id="task' + status_id + '_total"></span></td> \
                </tr>'
    total_row.before(row);

    //Rebind the event handlers
    var textFields = $("input[type=text]");
    textFields.change(function() {isPageChanged = true;});
    textFields.change(updateTotals);

    return row;
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
    textFields.change(function() {isPageChanged = true;});
    textFields.change(updateTotals);

    //Don't warn about leaving page if hitting "Save"
    $("input[type=submit]").click(function() {window.onbeforeunload = null;});
});
