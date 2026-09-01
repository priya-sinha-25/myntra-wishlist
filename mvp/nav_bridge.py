"""Navigation bridge — iframe JS updates Streamlit parent via query params."""

NAV_BRIDGE_JS = """
function mvpNavigate(params) {
  try {
    var u = new URL(window.parent.location.href);
    Object.keys(params).forEach(function(k) {
      var v = params[k];
      if (v === null || v === undefined || v === '') u.searchParams.delete(k);
      else u.searchParams.set(k, String(v));
    });
    window.parent.location.href = u.toString();
  } catch (e) {
    alert('Action failed — please refresh the page.');
  }
}
function mvpAddToBag(itemId, size, label) {
  mvpNavigate({bag_add: itemId, bag_size: size, bag_label: label, screen: 'bag'});
}
function mvpRemoveFromBag(itemId) {
  mvpNavigate({bag_remove: itemId, screen: 'bag'});
}
"""
