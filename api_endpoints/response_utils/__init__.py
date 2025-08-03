import codecs
from os import environ
from json import loads

__FIX_ESCAPE_TYPOS = environ.get("FIX_ESCAPE_TYPOS", "true").strip() == "true"


def fix_escaped_characters(text_with_errors: str) -> str:
    """
    Corrects specific "double-escaped" character sequences in a string.

    For example, '\\n' becomes '\n'.

    Args:
        text_with_errors: The input string with potential double-escaped sequences.

    Returns:
        A string with specific escape sequences corrected.
    """

    if not __FIX_ESCAPE_TYPOS:
        return text_with_errors
    if text_with_errors is None:
        return ""
    # Perform specific replacements
    fixed_text = text_with_errors
    fixed_text = fixed_text.replace("\\n", "\n")  # \n -> newline
    fixed_text = fixed_text.replace("\\t", "\t")  # \t -> tab
    fixed_text = fixed_text.replace('\\"', '"')  # \" -> "
    fixed_text = fixed_text.replace("\\'", "'")  # \' -> '

    return fixed_text


def load_json_with_fixed_escape(text_with_errors: str):
    if not __FIX_ESCAPE_TYPOS:
        return loads(text_with_errors)

    try:
        return loads(text_with_errors)
    except:
        return loads(fix_escaped_characters(text_with_errors))


if __name__ == "__main__":
    print(fix_escaped_characters("This should be a newline |\n|"))
    print(fix_escaped_characters("This should be a newline |\\n|"))
    print(fix_escaped_characters("This should be a tab |\t|"))
    print(fix_escaped_characters("This should be a tab |\\t|"))
    print(fix_escaped_characters("This should be a newline |\\n\\n|"))
    print(fix_escaped_characters("This should be a newline |\n\n|"))

    print(
        fix_escaped_characters(
            """
Tôi là Roo, một trợ lý kỹ thuật am hiểu, tập trung vào việc trả lời các câu hỏi và cung cấp thông tin về phát triển phần mềm, công nghệ và các chủ đề liên quan. Trong chế độ 'Hỏi' này, tôi có thể:
*   Trả lời các câu hỏi về phát triển phần mềm và công nghệ.
*   Cung cấp thông tin về các khái niệm, công cụ và phương pháp.
*   Sử dụng các công cụ để đọc tệp, tìm kiếm tệp, liệt kê tệp và định nghĩa mã.\\n\\n
*   Yêu cầu hướng dẫn cho các tác vụ cụ thể.
*   Hỏi bạn các câu hỏi tiếp theo nếu tôi cần thêm thông tin.
*   Đề xuất chuyển sang các chế độ khác (ví dụ: chế độ 'Mã' để thực hiện thay đổi mã).
Tôi sẵn sàng giúp bạn với các câu hỏi kỹ thuật của bạn.    
    """.strip()
        )
    )

    print(
        fix_escaped_characters(
            """
<thinking>
ユーザーは私が何ができるか尋ねています。私は技術アシスタントとして、ソフトウェア開発、テクノロジー、関連トピックに関する質問に答え、情報を提供することに焦点を当てています。私の能力と利用可能なツールについて説明する必要があります。
</thinking>
私はRooです。技術アシスタントとして、ソフトウェア開発、テクノロジー、関連トピックに関する質問に答え、情報を提供することに焦点を当てています。
\\n
\\t具体的には、以下のことができます。

*   **ファイルやディレクトリの操作:** ファイルの内容を読んだり、ディレクトリ内のファイルやディレクトリを一覧表示したりできます。
*   **コードの分析:** ソースコードの定義（クラス、関数など）をリストアップしたり、ファイル内の特定のパターンを検索したりできます。
*   **情報の検索:** ファイルシステム内で正規表現を使用して情報を検索できます。
*   **質問への回答:** ソフトウェア開発やテクノロジーに関する質問に答えることができます。
*   **タスクの実行:** ファイルの作成や編集など、特定のタスクを実行するためのツールを使用できます。ただし、現在の「Ask」モードではファイルの書き込みはできません。ファイルの書き込みが必要な場合は、「Code」モードなどの書き込み可能なモードに切り替える必要があります。
*   **指示の取得:** 特定のタスクを実行するための手順を取得できます。
*   **フォローアップ質問:** タスクを完了するために追加情報が必要な場合に、ユーザーに質問できます。

これらのツールと能力を組み合わせて、様々な技術的な課題を支援できます。何かお手伝いできることはありますか？    
    """.strip()
        )
    )
