function unselectAllButThis(items, i)
{
    for (let j = 0; j < items.length; j++)
    {
        if (i == j)
        {
            items[j].getElementsByTagName('a')[0].className = 'selected'
        }
        else
        {
            items[j].getElementsByTagName('a')[0].className = 'sheetsHost'
        }
    }
}

function onDomReady() {
    let verticalMenu = document.getElementById("verticalMenu");
    let menuItems = verticalMenu.children;
    for (let i = 0; i < menuItems.length; i++)
    {
        menuItems[i].onclick = function() { unselectAllButThis(menuItems, i); };
    }
}

$(onDomReady)