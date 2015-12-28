-module(tf_idf).
-export([tf_idf/1]).

%% Performs tf-idf on a collection of documents.

%% Uses term_freq/3 to get tuple of the freq dict and doc size
term_freq(Text) ->
    term_freq(Text, 0, dict:new()).

term_freq([], Sum, Dict) ->
    {Dict, Sum};

term_freq([Token|Rest], Sum, Dict) ->
    term_freq(Rest, Sum+1,
        dict:update_counter(Token, 1, Dict)).

inv_doc_freq(Docs) ->
    inv_doc_freq(Docs, 0, dict:new()).

inv_doc_freq([], DocNum, Dict) ->
    dict:map(
        fun(_Key, Value) -> math:log10(DocNum/Value) end,
        Dict);

inv_doc_freq([{Doc, _Sum}|Rest], DocNum, Dict) ->
    inv_doc_freq(Rest, DocNum+1,
        dict:fold(
            fun(Key, _Value, AccIn) ->
                    dict:update_counter(Key, 1, AccIn) end,
            Dict,
            Doc)
    ).

total_doc_size(Docs) ->
    lists:foldl(
        fun({_Doc, DocSum}, Total) -> Total + DocSum end,
        0,
        Docs).

total_token_freqs(Docs) ->
    lists:foldl(
        fun({Doc, _Sum}, Current) ->
                dict:fold(
                    fun(Key, Value, AccIn) ->
                            dict:update_counter(Key,Value,AccIn)
                    end,
                    Current,
                    Doc)
        end,
        dict:new(),
        Docs).

tf_idf(Docs) ->
    Idfs = inv_doc_freq(Docs),
    DocLen = total_doc_size(Docs),
    DocTotalFreqs = total_token_freqs(Docs),
    dict:map(
        fun(Key, Value) ->
                dict:fetch(Key, Idfs) * Value / DocLen
        end,
        DocTotalFreqs).

%% Adapted from
%% https://omlog.wordpress.com/2010/10/11/elegant-ir-with-erlang/

