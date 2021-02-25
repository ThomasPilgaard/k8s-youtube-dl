$(document).ready( function () {
    $('#jobs-table').DataTable({
        "bLengthChange": false,
        rowReorder: {
            selector: 'td:nth-child(0)'
        },
        responsive: true,
        "order": [[ 3, "desc" ]],
    });

    $('#workers-table').DataTable({
        "bLengthChange": false,
        rowReorder: {
            selector: 'td:nth-child(0)'
        },
        responsive: true,
    });
});
