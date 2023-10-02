from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QAction, QToolBar, \
    QLineEdit, QWidget, QVBoxLayout, QMenu, QDialog, QLabel
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QDesktopServices
import sys

class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
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

        # 검색 위젯 생성
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("검색 파일 또는 디렉터리")
        self.search_input.textChanged.connect(self.searchFiles)

        # 세부 정보 위젯 생성
        self.details_widget = QWidget(self)
        self.details_layout = QVBoxLayout(self.details_widget)

        # 툴바 생성
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # 뒤로 가기 버튼
        self.back_action = QAction("←", self)
        self.back_action.triggered.connect(self.goBack)
        toolbar.addAction(self.back_action)
        self.back_history = []

        # 앞으로 가기 버튼
        self.forward_action = QAction("→", self)
        self.forward_action.triggered.connect(self.goForward)
        toolbar.addAction(self.forward_action)
        self.forward_history = []

        # 상태 창 (경로 표시)
        self.status_bar = QLabel(self)
        toolbar.addWidget(self.status_bar)  # 상태 창을 툴바에 추가

        # 검색 결과를 저장하는 변수
        self.search_results = []

        # 컨텍스트 메뉴 생성
        self.context_menu = QMenu(self)
        self.view_details_action = QAction("상세 정보 보기", self)
        self.view_details_action.triggered.connect(self.showDetails)
        self.context_menu.addAction(self.view_details_action)

        # 트리뷰 우클릭 이벤트 핸들러 설정
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.showContextMenu)

        # QTreeView의 clicked 시그널에 updateStatusbar 메서드를 연결합니다.
        self.tree_view.clicked.connect(lambda index: self.updateStatusbar(index))

        # 메인 레이아웃 설정
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.search_input)
        layout.addWidget(self.tree_view)
        layout.addWidget(self.details_widget)
        self.setCentralWidget(central_widget)

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
        index = self.tree_view.currentIndex()
        if index.isValid():
            file_info = self.model.fileInfo(index)
            if file_info.exists():
                details_dialog = QDialog(self)
                details_dialog.setWindowTitle("상세 정보")
                layout = QVBoxLayout(details_dialog)

                file_name_label = QLabel(f"파일 이름: {file_info.fileName()}", details_dialog)
                layout.addWidget(file_name_label)

                file_size_label = QLabel(f"파일 크기: {file_info.size()} 바이트", details_dialog)
                layout.addWidget(file_size_label)

                file_path_label = QLabel(f"파일 경로: {file_info.filePath()}", details_dialog)
                layout.addWidget(file_path_label)

                details_dialog.exec_()

    def updateStatusbar(self, index):
        current_path = self.model.filePath(index)
        self.status_bar.setText(f"현재 경로: {current_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileExplorer()
    ex.show()
    sys.exit(app.exec_())




