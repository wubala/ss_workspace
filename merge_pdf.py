#!/usr/bin/python3
"""Merge two PDFs into one using CoreGraphics (macOS built-in)."""
import ctypes, ctypes.util, os, sys

libcg = ctypes.CDLL(ctypes.util.find_library('CoreGraphics'))

# CoreGraphics types
class CGPDFDocument(ctypes.Structure):
    pass

class CGRect(ctypes.Structure):
    _fields_ = [
        ('origin', ctypes.c_double * 2),
        ('size', ctypes.c_double * 2),
    ]

class CGSize(ctypes.Structure):
    _fields_ = [
        ('width', ctypes.c_double),
        ('height', ctypes.c_double),
    ]

# Function prototypes
CGPDFDocumentGetVersion = libcg.CGPDFDocumentGetVersion
CGPDFDocumentGetVersion.argtypes = [ctypes.POINTER(CGPDFDocument)]
CGPDFDocumentGetVersion.restype = None

CGPDFDocumentCreateWithURL = libcg.CGPDFDocumentCreateWithURL
CGPDFDocumentCreateWithURL.argtypes = [ctypes.c_void_p]
CGPDFDocumentCreateWithURL.restype = ctypes.POINTER(CGPDFDocument)

CGPDFDocumentGetPageCount = libcg.CGPDFDocumentGetPageCount
CGPDFDocumentGetPageCount.argtypes = [ctypes.POINTER(CGPDFDocument)]
CGPDFDocumentGetPageCount.restype = ctypes.c_int

CGPDFDocumentGetPage = libcg.CGPDFDocumentGetPage
CGPDFDocumentGetPage.argtypes = [ctypes.POINTER(CGPDFDocument), ctypes.c_int]
CGPDFDocumentGetPage.restype = ctypes.c_void_p

CGPDFPageGetBoxAngle = libcg.CGPDFPageGetBoxAngle
CGPDFPageGetBoxAngle.argtypes = [ctypes.c_void_p, ctypes.c_int]
CGPDFPageGetBoxAngle.restype = ctypes.c_double

CGPDFPageGetRect = libcg.CGPDFPageGetRect
CGPDFPageGetRect.argtypes = [ctypes.c_void_p, ctypes.c_int]
CGPDFPageGetRect.restype = CGRect

CGPDFPageGetDrawingTransform = libcg.CGPDFPageGetDrawingTransform
CGPDFPageGetDrawingTransform.argtypes = [ctypes.c_void_p, ctypes.c_int, CGRect, ctypes.c_int, ctypes.c_bool, ctypes.c_bool]
CGPDFPageGetDrawingTransform.restype = ctypes.c_void_p  # CGAffineTransform

CGRectMake = libcg.CGRectMake
CGRectMake.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
CGRectMake.restype = CGRect

CGSizeMake = libcg.CGSizeMake
CGSizeMake.argtypes = [ctypes.c_double, ctypes.c_double]
CGSizeMake.restype = CGSize

# CGAffineTransform
class CGAffineTransform(ctypes.Structure):
    _fields_ = [
        ('a', ctypes.c_double), ('b', ctypes.c_double),
        ('c', ctypes.c_double), ('d', ctypes.c_double),
        ('tx', ctypes.c_double), ('ty', ctypes.c_double),
    ]

# CGContext functions
CGContextNew = libcg.CGContextNew
CGContextNew.argtypes = [ctypes.c_void_p]  # CFMutableData or NULL
CGContextNew.restype = ctypes.c_void_p

kCGPDFContextMediaBox = 0  # approximate

# Actually let's use a simpler approach - write PDF manually
# macOS's CGContext has CGPDFContextCreate which can create PDF

CGContextBeginPage = libcg.CGContextBeginPage
CGContextBeginPage.argtypes = [ctypes.c_void_p, ctypes.POINTER(CGRect)]
CGContextBeginPage.restype = None

CGContextDrawPDFPage = libcg.CGContextDrawPDFPage
CGContextDrawPDFPage.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
CGContextDrawPDFPage.restype = None

CGContextEndPage = libcg.CGContextEndPage
CGContextEndPage.argtypes = [ctypes.c_void_p]
CGContextEndPage.restype = None

CGContextSaveGState = libcg.CGContextSaveGState
CGContextSaveGState.argtypes = [ctypes.c_void_p]
CGContextSaveGState.restype = None

CGContextRestoreGState = libcg.CGContextRestoreGState
CGContextRestoreGState.argtypes = [ctypes.c_void_p]
CGContextRestoreGState.restype = None

CGContextTranslateCTM = libcg.CGContextTranslateCTM
CGContextTranslateCTM.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double]
CGContextTranslateCTM.restype = None

CGContextScaleCTM = libcg.CGContextScaleCTM
CGContextScaleCTM.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double]
CGContextScaleCTM.restype = None

CGPDFContextCreate = libcg.CGPDFContextCreate
CGPDFContextCreate.argtypes = [ctypes.c_void_p, ctypes.POINTER(CGRect), ctypes.c_void_p]
CGPDFContextCreate.restype = ctypes.c_void_p

CGContextRelease = libcg.CGContextRelease
CGContextRelease.argtypes = [ctypes.c_void_p]
CGContextRelease.restype = None

def url_from_path(path):
    """Create a CFURL from a POSIX path."""
    cfurl = ctypes.CDLL(ctypes.util.find_library('CoreFoundation'))
    cfurl.CFURLCreateFromFileSystemRepresentation.argtypes = [
        ctypes.c_void_p,  # allocator (NULL = default)
        ctypes.c_char_p,
        ctypes.c_long,
        ctypes.c_bool
    ]
    cfurl.CFURLCreateFromFileSystemRepresentation.restype = ctypes.c_void_p
    url = cfurl.CFURLCreateFromFileSystemRepresentation(
        None, path.encode('utf-8'), len(path), True
    )
    return url

def merge_pdfs(pdf_paths, output_path):
    """Merge multiple PDFs into one using CoreGraphics."""
    
    pages_info = []
    for p in pdf_paths:
        url = url_from_path(p)
        doc = CGPDFDocumentCreateWithURL(url)
        if not doc:
            print(f"ERROR: Cannot open {p}")
            continue
        count = CGPDFDocumentGetPageCount(doc)
        print(f"  {p}: {count} page(s)")
        pages_info.append((doc, count))
    
    if not pages_info:
        print("No PDFs to merge!")
        return False
    
    # For A4 size in points (72 dpi)
    # A4: 595.28 x 841.89 points
    # We'll use letter size: 612 x 792
    page_w, page_h = 595.28, 841.89  # A4
    
    # Create PDF context
    url_out = url_from_path(output_path)
    
    # Use first page to determine size
    first_doc, _ = pages_info[0]
    first_page = CGPDFDocumentGetPage(first_doc, 1)
    first_rect = CGPDFPageGetRect(first_page, 0)  # kCGPDFMediaBox = 0
    pw = first_rect.size.width
    ph = first_rect.size.height
    print(f"  Page size: {pw:.1f} x {ph:.1f}")
    
    mediabox = CGRectMake(0, 0, pw, ph)
    pdf_ctx = CGPDFContextCreate(None, ctypes.byref(mediabox), None)
    
    if not pdf_ctx:
        print("ERROR: Cannot create PDF context")
        return False
    
    page_num = 0
    for doc, count in pages_info:
        for i in range(1, count + 1):
            page = CGPDFDocumentGetPage(doc, i)
            if not page:
                continue
            
            page_rect = CGPDFPageGetRect(page, 0)
            
            # Begin page
            CGContextBeginPage(pdf_ctx, ctypes.byref(page_rect))
            CGContextSaveGState(pdf_ctx)
            
            # Draw the PDF page
            CGContextDrawPDFPage(pdf_ctx, page)
            
            CGContextRestoreGState(pdf_ctx)
            CGContextEndPage(pdf_ctx)
            page_num += 1
            print(f"  Drew page {page_num}")
    
    CGContextRelease(pdf_ctx)
    print(f"Done! Merged {page_num} pages to {output_path}")
    return True

if __name__ == '__main__':
    pdfs = ['/Users/a1-6/Desktop/page1.pdf', '/Users/a1-6/Desktop/page2.pdf']
    out = '/Users/a1-6/Desktop/卷子合并.pdf'
    merge_pdfs(pdfs, out)
