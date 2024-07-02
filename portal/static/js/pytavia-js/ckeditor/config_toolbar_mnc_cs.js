/*
Custom configuration for CKEditor Rich Text Format

*/

CKEDITOR.editorConfig   = function( config ) {
    config.enterMode    = CKEDITOR.ENTER_BR;
    config.skin         = 'moono-lisa';
    //config.skin         = 'kama';
    
    config.toolbar      = [
        { name : 'clipboard',   items : [  'Undo', 'Redo','-','Cut', 'Copy', 'Paste', 'PasteText' ] },
        { name : 'editing',     items : [ 'Find', 'Replace', 'SelectAll',  '-', 'CopyFormatting', 'RemoveFormat' ] },
        { name : 'insert',      items : [ 'Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar'] },
        { name : 'links',       items : [ 'Link', 'Unlink'] },
        { name : 'document',    items : [ 'Source', 'Preview'] },
        { name : 'tools',       items : [ 'Maximize', 'ShowBlocks' ] },
        '/',
        { name : 'paragraph',   items : [ 'NumberedList', 'BulletedList', '-','JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock','-', 'Outdent', 'Indent', 'BidiLtr'] },
        { name : 'basicstyles', items : [ 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'] },
        { name : 'styles',      items : [ 'Styles', 'Format', 'Font', 'FontSize' ] },
        { name : 'colors',      items : [ 'TextColor', 'BGColor' ] },
        
    ];
};