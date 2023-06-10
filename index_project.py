from clang.cindex import CursorKind, Index, CompilationDatabase, Cursor
from pathlib import Path
import sys


def get_files(comp_db: CompilationDatabase) -> list[str]:
    files = []
    for ccd in comp_db.getAllCompileCommands():
        files.append(ccd.filename)
    return files


def get_args(comp_db: CompilationDatabase, filename: str) -> list[str]:
    ccds = comp_db.getCompileCommands(filename)
    ccd = list(ccds)[0]
    args = ccd.arguments
    # Skip first argument, guaranteed to be compiler name
    next(args)
    args_list = []
    for arg in args:
        # "-o" <output> <input>
        # Ignore these
        if arg == "-o":
            return args_list
        args_list.append(arg)
    # Ignore last argument, must be filename
    return args_list[:-1]


def get_called_func(cursor: Cursor) -> str:
    assert cursor.kind == CursorKind.CALL_EXPR
    for child in cursor.walk_preorder():
        if child.kind == CursorKind.DECL_REF_EXPR:
            ref = child.referenced
            if ref.kind == CursorKind.FUNCTION_DECL:
                return get_func_name(ref)


def get_func_name(cursor: Cursor) -> str:
    assert cursor.kind == CursorKind.FUNCTION_DECL
    # print(cursor.kind)
    sig = cursor.displayname
    return sig


def extract_calls(cursor: Cursor, file: str) -> str:
    kind = cursor.kind
    if file == cursor.extent.start.file.name:
        if kind == CursorKind.FUNCTION_DECL and cursor.is_definition():
            print("Def: ", get_func_name(cursor))
        elif kind == CursorKind.CALL_EXPR:
            print("  Call: ", get_called_func(cursor))
    for child in cursor.get_children():
        extract_calls(child, file)


idx = Index.create()
comp_db_path = sys.argv[1]
comp_db = CompilationDatabase.fromDirectory(comp_db_path)

files = get_files(comp_db)
for file in files:
    args = get_args(comp_db, file)
    tu = idx.parse(file, args)
    extract_calls(tu.cursor, file)