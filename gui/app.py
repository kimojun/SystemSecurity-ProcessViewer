from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QAction, QToolBar, \
    QLineEdit, QWidget, QVBoxLayout, QMenu, QDialog, QLabel, QPushButton, QDateEdit, QFileDialog , QInputDialog
from PyQt5.QtCore import QDir, Qt, QDate
from PyQt5.QtGui import QDesktopServices
import sys

class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ctrl_pressed = False  # 컨트롤 키가 눌려 있는지 확인
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("File Explorer")

        # 파일 시스템 모델 생성
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        # 파일 시스템 뷰 생성
        self.tree_view = QTreeView(self)
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(QDir.rootPath()))
        self.tree_view.setColumnWidth(0, 250)
        self.tree_view.setSelectionMode(QTreeView.ExtendedSelection)  # ExtendedSelection 모드로 설정

        # 검색 위젯 생성
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("검색 파일 또는 디렉터리")
        self.search_input.textChanged.connect(self.searchFiles)

        # 툴바 생성 전에 경로 입력 위젯 초기화
        self.path_input = QLineEdit(self)
        self.path_input.returnPressed.connect(self.navigateToPath)  # 엔터 키 이벤트 연결

        # 툴바 생성
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        self.back_action = QAction("←", self)
        self.back_action.triggered.connect(self.goBack)
        toolbar.addAction(self.back_action)
        self.forward_action = QAction("→", self)
        self.forward_action.triggered.connect(self.goForward)
        toolbar.addAction(self.forward_action)


        self.context_menu = QMenu(self)
        self.view_details_action = QAction("상세 정보 보기", self)
        self.view_details_action.triggered.connect(self.showDetails)
        self.context_menu.addAction(self.view_details_action)

        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.showContextMenu)
        self.tree_view.clicked.connect(lambda index: self.updateStatusbar(index))

        # 중앙 위젯 설정
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.search_input)
        layout.addWidget(self.tree_view)
        self.setCentralWidget(central_widget)

        # 현재 경로 표시 및 수정
        self.path_input = QLineEdit(self)
        self.path_input.returnPressed.connect(self.navigateToPath)  # 엔터 키 이벤트 연결
        toolbar.addWidget(self.path_input)  # 입력란을 툴바에 추가

    def navigateToPath(self):
        path = self.path_input.text()
        index = self.model.index(path)
        if index.isValid():
            self.tree_view.setRootIndex(index)
            self.updateStatusbar(index)
        else:
            # 유효하지 않은 경로에 대한 오류 처리
            pass


    def goBack(self):
        if self.back_history:
            self.forward_history.append(self.tree_view.rootIndex())
            self.tree_view.setRootIndex(self.back_history.pop())
            self.updateStatusbar(self.tree_view.rootIndex())

    def goForward(self):
        if self.forward_history:
            self.back_history.append(self.tree_view.rootIndex())
            self.tree_view.setRootIndex(self.forward_history.pop())
            self.updateStatusbar(self.tree_view.rootIndex())

    def searchFiles(self):
        query = self.search_input.text()
        if query:
            root_index = self.tree_view.rootIndex()
            self.search_results = []
            self.findFiles(root_index, query)
            self.updateTreeView()
            self.updateStatusbar(root_index)

    def findFiles(self, index, query):
        if index.isValid():
            if query.lower() in self.model.fileName(index).lower():
                self.search_results.append(index)
            if self.model.isDir(index):
                for i in range(self.model.rowCount(index)):
                    child_index = self.model.index(i, 0, index)
                    self.findFiles(child_index, query)

    def updateTreeView(self):
        self.tree_view.setModel(None)
        self.model.setNameFilters([])
        self.model.setRootPath("")
        self.model.setNameFilters(['*'])
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.tree_view.model().index(QDir.rootPath()))
        for index in self.search_results:
            self.tree_view.expand(index)

    def showContextMenu(self, pos):
        index = self.tree_view.indexAt(pos)
        if index.isValid():
            self.context_menu.exec_(self.tree_view.mapToGlobal(pos))

    def showDetails(self):
        # 상세 정보 창 표시 메서드
        index = self.tree_view.currentIndex()
        if index.isValid():
            file_info = self.model.fileInfo(index)
            if file_info.exists():
                details_dialog = QDialog(self)
                layout = QVBoxLayout(details_dialog)
                file_name_label = QLabel(f"파일 이름: {file_info.fileName()}", details_dialog)
                layout.addWidget(file_name_label)
                file_size_label = QLabel(f"파일 크기: {file_info.size()} 바이트", details_dialog)
                layout.addWidget(file_size_label)
                file_path_label = QLabel(f"파일 경로: {file_info.filePath()}", details_dialog)
                layout.addWidget(file_path_label)
                last_modified_label = QLabel(f"마지막 변경날짜: {file_info.lastModified().toString()}", details_dialog)
                layout.addWidget(last_modified_label)
                last_accessed_label = QLabel(f"마지막 접근날짜: {file_info.lastRead().toString()}", details_dialog)
                layout.addWidget(last_accessed_label)
                created_label = QLabel(f"생성 날짜: {file_info.birthTime().toString()}", details_dialog)
                layout.addWidget(created_label)
                details_dialog.exec_()

    def updateStatusbar(self, index):
        current_path = self.model.filePath(index)
        self.path_input.setText(current_path)  # 경로를 QLineEdit 위젯에 설정

    '''
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.ctrl_pressed = True
            self.tree_view.setSelectionMode(QTreeView.MultiSelection)
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.ctrl_pressed = False
            self.tree_view.setSelectionMode(QTreeView.SingleSelection)
        super().keyReleaseEvent(event)
    '''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileExplorer()
    ex.show()
    sys.exit(app.exec_())




