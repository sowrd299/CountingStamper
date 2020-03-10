// this makes all of the "topics" into collapsible sections
// originally from: https://github.com/sowrd299/LangSite/blob/master/articles/static/articles/collapsible.js

// collapses or un-collapses the specified object
function toggle_collapse(target){
    if(target in cached_collapse_status){
        // handle interacting with temp expansion
        if(cached_collapse_status[target] === "none"){
            cached_collapse_status[target] = "block";
        }else{
            cached_collapse_status[target] = "none";
        }
    }else{
        if(target.style.display === "none"){
            target.style.display = "block";
        }else{
            target.style.display = "none";
        }
    }
}

// collapses or un-collapses the object with the target id
function toggle_collapse_id(target_id){
    toggle_collapse(document.getElementById(target_id));
}

// a dict of temp_expanded_object : cached status
var cached_collapse_status = {};

// temporily forces a section to expand
// reverts to previous state after end_temp_expand is called
function temp_expand(target){
    cached_collapse_status[target] = target.style.display;
    target.style.display = "block";
}

function temp_expand_id(target_id){
    temp_expand(document.getElementById(target_id));
}

function end_temp_expand(target){
    target.style.display = cached_collapse_status[target];
    delete[cached_collapse_status[target]];
}

function end_temp_expand_id(target_id){
    end_temp_expand(document.getElementById(target_id));
}