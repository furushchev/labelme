from qtpy import QtWidgets


class LabelQListWidget(QtWidgets.QListWidget):

    def __init__(self, *args, **kwargs):
        super(LabelQListWidget, self).__init__(*args, **kwargs)
        self.canvas = None
        self.itemsToShapes = []
        self.toggleSort(kwargs.get('sort', False))

    def get_shape_from_item(self, item):
        for index, (item_, shape) in enumerate(self.itemsToShapes):
            if item_ is item:
                return shape

    def get_item_from_shape(self, shape):
        for index, (item, shape_) in enumerate(self.itemsToShapes):
            if shape_ is shape:
                return item

    def clear(self):
        super(LabelQListWidget, self).clear()
        self.itemsToShapes = []

    def setParent(self, parent):
        self.parent = parent

    def toggleSort(self, value):
        self.sortEnabled = value
        if value:
            self.setDragDropMode(
                QtWidgets.QAbstractItemView.NoDragDrop)
            self.sortItems()
        else:
            self.setDragDropMode(
                QtWidgets.QAbstractItemView.InternalMove)

    def dropEvent(self, event):
        shapes = self.shapes
        super(LabelQListWidget, self).dropEvent(event)
        if self.shapes == shapes:
            return
        if self.canvas is None:
            raise RuntimeError('self.canvas must be set beforehand.')
        self.parent.setDirty()
        self.canvas.loadShapes(self.shapes)

    @property
    def shapes(self):
        shapes = []
        for i in range(self.count()):
            item = self.item(i)
            shape = self.get_shape_from_item(item)
            shapes.append(shape)
        return shapes

    def addItem(self, item):
        retval = super(LabelQListWidget, self).addItem(item)
        if self.sortEnabled:
            self.sortItems()
        return retval

    def addItems(self, items):
        retval = super(LabelQListWidget, self).addItems(items)
        if self.sortEnabled:
            self.sortItems()
        return retval

    def takeItem(self, index):
        retval = super(LabelQListWidget, self).takeItem(index)
        if self.sortEnabled:
            self.sortItems()
        return retval
