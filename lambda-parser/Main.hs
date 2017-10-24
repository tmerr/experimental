{-# LANGUAGE TemplateHaskell, NoMonomorphismRestriction, RelaxedPolyRec #-}
module Main where

import Prelude (Show (..), Eq (..), String, ($), fst, Char, IO, putStrLn,
               (&&), (++))
import Data.Char (isLetter)
import Data.List (head)

import Control.Isomorphism.Partial
import Control.Isomorphism.Partial.TH
import Control.Isomorphism.Partial.Unsafe (Iso (Iso))
import Control.Isomorphism.Partial.Derived (foldl)
import Text.Syntax
import Text.Syntax.Printer.Naive
import Text.Syntax.Parser.Naive
import Data.Maybe

data Term
    = Variable String
    | Abstraction String Term
    | Application Term Term
  deriving (Show, Eq)

$(defineIsomorphisms ''Term)

letter :: Syntax delta => delta Char
letter = subset (\t -> isLetter t && t /= 'λ') <$> token
ident = many1 letter

lambda, thedot :: Syntax delta => delta ()
lambda = text "λ" <|> text "\\"
thedot = text "."

parens :: Syntax delta => delta Term -> delta Term
parens = between (text "(") (text ")")

innerTerm, term :: Syntax delta => delta Term
innerTerm =  variable <$> ident
         <|> parens term
term =  lambda *> (abstraction <$> ident <*> thedot *> sepSpace *> term)
    <|> (foldl application) <$> innerTerm <*> many (sepSpace *> innerTerm)

print_test :: String
print_test = fromMaybe "couldn't print" $ print term
    (Application (Abstraction "x" (Variable "x")) (Abstraction "y" (Variable "y")))

parse_test :: String
parse_test = show $ head $ parse term "λa. (λb. a (b c) d e)"

main :: IO ()
main = putStrLn $ "parse test: " ++ parse_test ++ "\nprint test: " ++ print_test
