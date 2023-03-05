#!/bin/sh

#  id2phone.R
#  
#
#  Created by Eleanor Chodroff on 3/24/15.
#
phones <- read.table("../../data/lang/phones.txt", quote="\"")
segments <- read.table("../../data/alignme/segments", quote="\"")
ctm <- read.table("./merged_alignment.txt", quote="\"")

names(ctm) <- c("file_utt","utt","start","dur","id")
ctm$file <- gsub("_[0-9]*$","",ctm$file_utt)
names(phones) <- c("phone","id")
names(segments) <- c("file_utt","file","start_utt","end_utt")

ctm2 <- merge(ctm, phones, by="id")
ctm3 <- merge(ctm2, segments, by=c("file_utt"))
ctm3$start_real <- ctm3$start + ctm3$start_utt
ctm3$end_real <- ctm3$start_utt + ctm3$dur

print(nrow(ctm2))

write.table(ctm3, "./final_ali.txt", row.names=F, quote=F, sep="\t")

