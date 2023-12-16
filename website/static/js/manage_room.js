$('#modRoom').on('click', function(){
    let id_room = $(this).data('id');
    $('#mod-id-room').val(id_room);
    console.log(id_room)
})

function submit_delete() {
    $('#deleteRoomForm').submit()
}
