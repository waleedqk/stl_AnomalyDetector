# stl_AnomalyDetector
  Using ANTLR4








https://stackoverflow.com/questions/41017948/antlr4-the-following-sets-of-rules-are-mutually-left-recursive

ANTLR4 supports only direct left recursion (which is already an improvement over previous versions). That means you can have left recursion in a single rule, but not over multiple rules (e.g. rule a uses rule b which uses a as the first rule in an alternative.
